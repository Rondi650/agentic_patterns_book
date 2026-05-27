class LoanApprovalAgent:
    CONFIDENCE_THRESHOLD = 0.95

    def process_application(self, application_data):
        # ... initial processing steps ...

        # Analyze property appraisal
        property_analysis = self.analyze_property(application_data.appraisal)

        if property_analysis['confidence'] < self.CONFIDENCE_THRESHOLD:
            # 1. Package the context for human review
            review_package = {
                "application_id": application_data.id,
                "issue": "Property data discrepancy",
                "details": property_analysis['details']
            }

            # 2. Call the human review system and pause
            human_decision = HumanReviewSystem.request_decision(review_package)

            # 3. Act on the human's decision
            if human_decision['action'] == "VALIDATE_APPRAISAL":
                self.log("Human validated appraisal. Resuming process.")
                # ... continue processing ...
                return "Status: Approved"
            else:
                self.log("Human rejected appraisal. Halting process.")
                return "Status: Rejected by Underwriter"

        else:
            # ... continue with high-confidence automated processing ...
            return "Status: Approved"


class HumanReviewSystem:
    @staticmethod
    def request_decision(package):
        # In a real system, this would push to a UI and wait for a callback.
        # Here, we simulate the human's response.
        print(f"--> Escalation sent to Human Review Dashboard: {package['issue']}")
        return {"action": "VALIDATE_APPRAISAL"}