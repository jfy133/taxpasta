# Copyright (c) 2022 Moritz E. Beber
# Copyright (c) 2022 Maxime Borry
# Copyright (c) 2022 James A. Fellows Yates
# Copyright (c) 2022 Sofia Stamouli.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a standardisation service for metaphlan profiles."""


import logging

import pandas as pd
import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application.service import ProfileStandardisationService
from taxpasta.domain.model import StandardProfile

from .metaphlan_profile import MetaphlanProfile


logger = logging.getLogger(__name__)


class MetaphlanProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for metaphlan profiles."""

    # Metaphlan only reports up to six decimals so this number should be large enough.
    LARGE_INTEGER = int(1e6)

    @classmethod
    @pa.check_types(lazy=True)
    def transform(
        cls, profile: DataFrame[MetaphlanProfile]
    ) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given metaphlan profile.

        Args:
            profile: A taxonomic profile generated by metaphlan.

        Returns:
            A standardized profile.

        """
        result = (
            profile[[MetaphlanProfile.ncbi_tax_id, MetaphlanProfile.relative_abundance]]
            .copy()
            .rename(
                columns={
                    MetaphlanProfile.ncbi_tax_id: StandardProfile.taxonomy_id,
                    MetaphlanProfile.relative_abundance: StandardProfile.count,
                }
            )
            .assign(
                **{
                    StandardProfile.taxonomy_id: lambda df: df[
                        StandardProfile.taxonomy_id
                    ]
                    .str.rsplit("|", n=1)
                    .str[-1],
                    StandardProfile.count: lambda df: df[StandardProfile.count]
                    * cls.LARGE_INTEGER,
                }
            )
            .assign(
                **{
                    StandardProfile.count: lambda df: df[StandardProfile.count].astype(
                        int
                    )
                }
            )
        )
        result[StandardProfile.taxonomy_id] = pd.to_numeric(
            result[StandardProfile.taxonomy_id], errors="coerce"
        ).astype("Int64")
        unclassified_mask = result[StandardProfile.taxonomy_id].isna() | (
            result[StandardProfile.taxonomy_id] == -1
        )
        num = int(unclassified_mask.sum())
        if num > 0:
            logger.warning(
                "Combining %d entries with unclassified taxa in the profile.", num
            )
        return pd.concat(
            [
                result.loc[~unclassified_mask, :],
                pd.DataFrame(
                    {
                        StandardProfile.taxonomy_id: [0],
                        StandardProfile.count: [
                            result.loc[unclassified_mask, StandardProfile.count].sum()
                        ],
                    },
                    dtype=int,
                ),
            ],
            ignore_index=True,
        )
