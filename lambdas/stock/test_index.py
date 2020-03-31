import index
import test_object as scenario

def monkey_patching():
    pass

def test_post_quote(event):
    return index.handler(event, {})

if __name__ == "__main__":
    monkey_patching()
   # print(test_post_quote(scenario.post_quote_symbol_date_price))
    #val = test_post_quote(scenario.get_company_symbol)
    val_1 = test_post_quote(scenario.get_quote_data_time_and_symbol)
    #print(val)
    print(val_1)
