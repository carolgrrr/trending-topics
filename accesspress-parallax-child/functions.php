<?php
add_action( 'wp_enqueue_scripts', 'my_theme_enqueue_styles' );
add_action( 'wp_enqueue_scripts', 'wpb_adding_scripts' );  

function my_theme_enqueue_styles() {
    wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' );

}

function wpb_adding_scripts() {
  wp_register_script('my_amazing_script', get_template_directory_uri() . '/my-script.js', array('jquery'),'1.1', false);
  wp_enqueue_script('my_amazing_script');
}

?>