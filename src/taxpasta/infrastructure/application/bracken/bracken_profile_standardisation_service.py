# Copyright (c) 2022, Moritz E. Beber, Maxime Borry, Sofia Stamouli.
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


"""Provide a standardisation service for Bracken profiles."""


import pandera as pa
from pandera.typing import DataFrame

from taxpasta.application.service import ProfileStandardisationService
from taxpasta.domain.model import StandardProfile

from .bracken_profile import BrackenProfile


class BrackenProfileStandardisationService(ProfileStandardisationService):
    """Define a standardisation service for Bracken profiles."""

    @classmethod
    @pa.check_types(lazy=True)
    def transform(
        cls, profile: DataFrame[BrackenProfile]
    ) -> DataFrame[StandardProfile]:
        """
        Tidy up and standardize a given Bracken profile.

        Args:
            profile: A taxonomic profile generated by Bracken.

        Returns:
            A standardized profile.

        Raises:
            pandera.errors.SchemaErrors: If the given profile does not conform with the
                `BrackenProfile` or the transformed output does not conform with the
                `StandardProfile`.  # noqa: DAR402

        """
        result = profile[
            [BrackenProfile.taxonomy_id, BrackenProfile.new_est_reads]
        ].copy()
        result.columns = [StandardProfile.taxonomy_id, StandardProfile.count]
        return result
