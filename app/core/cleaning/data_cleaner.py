class DataCleaning:

    @staticmethod
    def clean_rating(raw_rating: str = None) -> float:
        if raw_rating == "" or raw_rating is None:
            return 0
        rating_float = float(raw_rating)
        return rating_float

    @staticmethod
    def clean_review(raw_review: str = None) -> int:
        if raw_review == None:
            return 0
        if raw_review == "":
            return 0
        review_count = ""
        for i in raw_review:
            if i <= "9" and i >= "0":
                review_count += i
        return int(review_count)
