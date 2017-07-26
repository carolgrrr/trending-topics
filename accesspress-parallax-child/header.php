<?php
/**
 * The header for our theme.
 *
 * Displays all of the <head> section and everything up till <div id="content">
 *
 * @package accesspress_parallax
 */


	global $page_template;
	global $posttype;
	$posttype = get_post_type ($post->ID);
	$page_template = get_page_template_slug( $post->ID );
?>

<!DOCTYPE html>

<html <?php language_attributes(); ?>>

<head>

	<?php

	if (is_page(41461)) {
		echo '<script language="javascript">';
		echo 'alert("inside conditional include")';
		echo '</script>';
	}
	?>

<meta charset="<?php bloginfo( 'charset' ); ?>">

<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- <title><?php wp_title( '|', true, 'right' ); ?></title> -->

<link rel="profile" href="http://gmpg.org/xfn/11">
<link rel="pingback" href="<?php bloginfo( 'pingback_url' ); ?>">

<link rel="icon" href="/favicon.ico" type="image/x-icon" />

<link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />

<!--[if lt IE 9]>

	<script src="<?php echo get_template_directory_uri(); ?>/js/html5shiv.js"></script>

<![endif]-->


<?php wp_head(); ?>


	<?php
	if ($page_template == "template-carol.php") 
	{ 
	?>
		 
		<script>
		  jQuery(document).ready(function($){   
		    $( "#accordion" ).accordion();
		  } );
	  	</script>

	<?php  
	}
	?>

<script>

jQuery(document).ready(function($){    

    $('#advancedOptions').hide();

    $('.foldable_div').click(function(){

        $('#advancedOptions').slideToggle('slow');        

    });

});

</script>

</head>



<body <?php body_class(); ?>>

<div id="page" class="hfeed site">

	<header id="masthead" class="<?php echo of_get_option('header_layout'); ?>">

		<div class="mid-content clearfix">

		<div id="site-logo">

		<?php if ( get_header_image() ) : ?>

		<a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home">

			<img src="<?php header_image(); ?>" alt="<?php bloginfo( 'name' ); ?>">

		</a>

		<?php else:?>

			<h1 class="site-title"><a href="<?php echo esc_url( home_url( '/' ) ); ?>" rel="home"><?php bloginfo( 'name' ); ?></a></h1>

			<h2 class="site-description"><?php bloginfo( 'description' ); ?></h2>

		<?php endif; ?>

		</div>



		<nav id="site-navigation" class="main-navigation">

		<div class="menu-toggle"><?php _e( 'Menu', 'accesspress_parallax' ); ?></div>

					

			<?php 

			$sections = of_get_option('parallax_section');

			//if(of_get_option('enable_parallax')!=1 && of_get_option('enable_parallax_nav')!=1): 

			if(of_get_option('enable_parallax_nav')!=1): 

				wp_nav_menu( array( 

					'theme_location' => 'primary' , 

					'container'      => '',

					'menu_class'      => 'nav',

					'fallback_cb'     => '',

					) );

			else: ?>

				<ul class="nav single-page-nav">

				<?php

				$home_text = of_get_option('home_text');

					if(of_get_option('show_slider')== "yes" && !empty($home_text)) : ?>

						<li class="current"><a href="<?php echo esc_url( home_url( '/' ) ); ?>#main-slider"><?php echo esc_attr($home_text); ?></a></li>

					<?php endif;

					

					if(!empty($sections)):

					foreach ($sections as $single_sections): 

						if($single_sections['layout'] != "action_template" && $single_sections['layout'] != "blank_template" && $single_sections['layout'] != "googlemap_template" && !empty($single_sections['page'])) :

						$title = get_the_title($single_sections['page']); ?>

						<li><a href="<?php echo esc_url( home_url( '/' ) ); ?>#section-<?php echo $single_sections['page']; ?>"><?php echo $title; ?></a></li>

						<?php 

						endif;

					endforeach; 

					endif; ?>

				</ul>

			<?php

			endif; ?>			

		</nav><!-- #site-navigation -->

			

		





		<?php 

		if(of_get_option('show_social') == 1):

			do_action('accesspress_social');

		endif; ?>

	</header><!-- #masthead -->



	<?php 

	$accesspress_show_slider = of_get_option('show_slider') ;

	$content_class = "";

	if(empty($accesspress_show_slider) || $accesspress_show_slider == "no"):

		$content_class = "no-slider";

	endif;

	?>

	<div id="content" class="site-content <?php echo $content_class; ?>">

	<?php 

	if(is_home() || is_front_page()) :

		do_action('accesspress_bxslider'); 

	endif;

	?>

