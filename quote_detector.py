



#created a dictionary in order to keep track of the word and vallue it is connected to


QUOTE_KEYWORDS = {
    "quote":3,
    "Quote":3,
    "rfq":3,
    "RFQ":3,
    "Rfq":3,
    "request for quote":3,
    "can you quote":3,
    "Please Quote":3,
    "Emely":3,
    "need a quote":3,
    "pricing":2,
    "Price":2,
    "price":2,
    "estimate":2,
    "how much":2,
    "quantity":2,
    "qty":2,
    "drawing":2,
    "attached":2,
        "pieces":1,
    "cost":1,
    "how much":1,
    "parts":1,

}
#gets our score 
def get_quote_score(subject,body):
    #takes in our subject and body and converts to lower 
    text = f"{subject} {body}".lower()

    score= 0
    #for phrase and points in our dictionary 
    for phrase, points in QUOTE_KEYWORDS.items():
        if phrase in text: #if there are phrases 
            score += points #we add the points 

    return score 



def is_quote_request(subject, body):
    score = get_quote_score(subject,body)

    if score >= 3:
        return True 

    return False 

if __name__ == "__main__":
    test_subject = "Bracket drawing"
    test_body = "Hello, can you quote 50 pieces? Drawing is attached"
    score = get_quote_score(test_subject,test_body)
    result = is_quote_request(test_subject, test_body)
    print(f"Quotw score: {score}")
    print(f"quote request: {result}")
