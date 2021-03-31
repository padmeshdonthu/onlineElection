class Election:
    def __init__(self, election_id, election_type, election_text, election_title, election_candidates,
                 election_start_date, election_end_date, results_published, can_publish="N"):
        self.election_id = election_id
        self.election_type = election_type
        self.election_text = election_text
        self.election_title = election_title
        self.election_candidates = election_candidates
        self.start_date = election_start_date
        self.end_date = election_end_date
        self.results_published = results_published
        self.can_publish = can_publish

    def calculate_winner(self, election_id):
        pass
        # check if date is crossing the end date and then calculate the winner for a particular election id
