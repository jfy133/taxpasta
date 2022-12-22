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


"""Provide a TSV reader."""


import pandas as pd

from taxpasta.application.service import BufferOrFilepath, TableReader


class TSVTableReader(TableReader):
    """Define the TSV reader."""

    @classmethod
    def read(cls, source: BufferOrFilepath, **kwargs) -> pd.DataFrame:
        """Read TSV from the given source."""
        return pd.read_table(source, sep="\t", **kwargs)
