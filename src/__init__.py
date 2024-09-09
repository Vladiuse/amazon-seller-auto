from src.application.amazon_product_collector.utils import retry


@retry(
    attempts=1,
    delay=1,
    exceptions=[ZeroDivisionError],
)
def test():
    print('test')
    raise ZeroDivisionError




print(test())