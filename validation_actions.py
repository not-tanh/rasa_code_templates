from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


class ValidateInquiryForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_inquiry_form"

    @staticmethod
    def account_number_db() -> List[Text]:
        return ["012345678912", "012345678913", "012345678914"]

    def validate_account_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        if slot_value.lower() in self.account_number_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"account_number": slot_value}
        else:
            # validation failed, set this slot to None so that the user will be asked for the slot again
            return {"account_number": None}
