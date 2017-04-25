import configparser
from woocommerce import API


def main():
	config = configparser.ConfigParser()
	config.read('settings.cfg')

	wcapi = API(
    	url=config.get('wordpress', 'url'), # Your store URL
    	consumer_key=config.get('wordpress', 'consumer_key'), # Your consumer key
    	consumer_secret=config.get('wordpress', 'consumer_secret'), # Your consumer secret
    	wp_api=True, # Enable the WP REST API integration
    	version="wc/v2", # WooCommerce WP REST API version
    	verify_ssl=False
	)


	print(wcapi)
	print(wcapi.get("customers/2"))
	#print(wcapi.get('orders/40856').json())

	#print(wcapi.get('orders/40856'))

	#/wp-json/wc/v2/orders
	#data = {
	#	"id": 123
	#	"line_items": [
    #    {
    #        "product_id": 93,
    #        "quantity": 10
    #    }
    #	]
	#}

	#print(wcapi.post('orders', data).json())


if __name__ == "__main__":
	main()