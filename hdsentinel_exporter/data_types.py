import re
from typing import Optional

import pydantic


class HardDiskSummary(pydantic.BaseModel):
    Hard_Disk_Number: Optional[int]
    Interface: Optional[str]
    Disk_Controller: Optional[str]
    Disk_Location: Optional[str]
    Hard_Disk_Model_ID: str
    Firmware_Revision: Optional[str]
    Hard_Disk_Serial_Number: str
    SSD_Controller: Optional[str]
    Total_Size: Optional[float]
    Power_State: Optional[str]
    Logical_Drive_s: Optional[str]
    Current_Temperature: float
    Maximum_Temperature_ever_measured: float
    Minimum_Temperature_ever_measured: float
    Daily_Average: float
    Daily_Maximum: float
    Power_on_time: Optional[str]
    Estimated_remaining_lifetime: Optional[str]
    Health: float
    Performance: float
    Description: Optional[str]
    Tip: Optional[str]
    disk_id: Optional[str]

    @pydantic.validator(
        'Total_Size',
        'Current_Temperature',
        'Maximum_Temperature_ever_measured',
        'Minimum_Temperature_ever_measured',
        'Daily_Average',
        'Daily_Maximum',
        'Health',
        'Performance',
        pre=True,
    )
    def convert_to_float(cls, value) -> float:
        match = re.match(r'^\d+(\.\d+)?', value)
        if match is None:
            raise ValueError(f'{value} is not a supported temperature.')
        return float(match.group())

    @pydantic.validator(
        'Health',
        'Performance',
    )
    def convert_percents_to_ratio(cls, value) -> float:
        return value / 100

    @pydantic.root_validator
    def set_harddisk_id(cls, values) -> dict:
        values['disk_id'] = f'{values["Hard_Disk_Model_ID"]} - {values["Hard_Disk_Serial_Number"]}'
        return values
