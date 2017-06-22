<?php

/**
 * The plugin bootstrap file
 *
 * This file is read by WordPress to generate the plugin information in the plugin
 * admin area. This file also includes all of the dependencies used by the plugin,
 * registers the activation and deactivation functions, and defines a function
 * that starts the plugin.
 *
 * @link              https://www.connectedaction.net/
 * @since             1.0.0
 * @package           add-trends-2-cart
 *
 * @wordpress-plugin
 * Plugin Name:       add-trends-2-cart
 * Plugin URI:        https://www.connectedaction.net/
 * Description:       This plugin allows Twitter search maps to be added to the Connected Action WooCommerce shopping cart by selecting check boxes and clicking a submit button.
 * Version:           1.0.0
 * Author:            Carol Schmitz
 * Author URI:        https://github.com/carolgrrr
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 * Text Domain:       add-trends-2-cart
 * Domain Path:       /languages
 */

// If this file is called directly, abort.
if ( ! defined( 'WPINC' ) ) {
	die;
}

/**
 * The code that runs during plugin activation.
 * This action is documented in includes/class-plugin-name-activator.php
 */
function activate_add_trends_2_cart() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-add-trends-2-cart-activator.php';
	Add_Trends_2_Cart_Activator::activate();
}

/**
 * The code that runs during plugin deactivation.
 * This action is documented in includes/class-plugin-name-deactivator.php
 */
function deactivate_add_trends_2_cart() {
	require_once plugin_dir_path( __FILE__ ) . 'includes/class-add-trends-2-cart-deactivator.php';
	Add_Trends_2_Cart_Deactivator::deactivate();
}

register_activation_hook( __FILE__, 'activate_add_trends_2_cart' );
register_deactivation_hook( __FILE__, 'deactivate_add_trends_2_cart' );

/**
 * The core plugin class that is used to define internationalization,
 * admin-specific hooks, and public-facing site hooks.
 */
require plugin_dir_path( __FILE__ ) . 'includes/class-add-trends-2-cart.php';

/**
 * Begins execution of the plugin.
 *
 * Since everything within the plugin is registered via hooks,
 * then kicking off the plugin from this point in the file does
 * not affect the page life cycle.
 *
 * @since    1.0.0
 */
function run_add_trends_2_cart() {

	$plugin = new Add_Trends_2_Cart();
	$plugin->run();

}
run_add_trends_2_cart();
