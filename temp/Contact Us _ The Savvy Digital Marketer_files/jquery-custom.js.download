( function ( $ ) {
    "use strict";

    /**
    * Loading bar
    */
    $( window ).on( 'load', function() {
        $( '#loading' ).fadeOut( 'slow' );
    } );

    /**
     * Keyboard Navigation
     */

    // If Tab key pressed
    $( '.menu-item-has-children' ).on( {
        keyup: function( e ) {
            var keyCode = e.keyCode || e.which;
            if (keyCode == 9) {
                $( this ).children( 'ul' ).addClass( 'is-focused' );
            }
        }
    } );

    // If Tab + Shift key pressed
    $( '.menu-item-has-children' ).keydown(function(e) {
        if( e.which  == 9 && e.shiftKey ){
            $( this ).children( '.sub-menu' ).removeClass( 'is-focused' );
        }
    } );

    // If focuse out
    $( '.menu-item-has-children .sub-menu' ).focusout(function( e ){
        if ( $( this ).children('.menu-item-has-children').length === 0 ) {
            $( this ).removeClass( 'is-focused' );
            $( this ).parents( '.is-focused' ).removeClass( 'is-focused' );
        }
    } );

    /**
     * Mobile menu
     */

    $( '.js-blank-loop' ).focusin( function(){
        $( '.mobile-nav>li:first-child a' ).focus();
    } );

    $( '.mobile-nav>li:first-child a' ).keydown(function(e) {
        if( e.which  == 9 && e.shiftKey ){
            e.preventDefault();
            $( this ).parents( '.mobile-nav' ).siblings( '.js-ct-menubar-close' ).focus();
        }
    } );

    jQuery( document ).ready( function( $ ) {
        $( '.dropdown-toggle' ).on( 'click', function(){
            $( this ).toggleClass( 'toggled' );
            $( this ).next().slideToggle();
        } );

        // Function to show the menu
        function show_menu( e ) {
            $( '.nav-parent' ).addClass( 'mobile-menu-open' );
            $( '.mobile-menu-overlay' ).addClass( 'mobile-menu-active' );
        }

        // Function to hide the menu
        function hide_menu(){
            $( '.nav-parent' ).removeClass( 'mobile-menu-open' );
            $( '.mobile-menu-overlay' ).removeClass( 'mobile-menu-active' );
        }

        // On Tab Press Open Menu ( Enter Press )
        $( '.js-ct-menubar-right' ).on( 'keyup keydown', function( e ) {
            var keyCode = e.keyCode || e.which;
            if (keyCode == 13) {
                e.preventDefault();
                show_menu();
            }
        } );

        // On Tab Press Close Menu ( Enter Press )
        $( '.js-ct-menubar-close' ).on( 'keyup keydown', function( e ) {
            var keyCode = e.keyCode || e.which;
            if (keyCode == 13) {
                e.preventDefault();
                hide_menu();
            }
        } );

        // Hide menu on escape press
        $('body').on( 'keyup keydown', function( e ) {
            var keyCode = e.keyCode || e.which;
            if (keyCode == 27) {
                hide_menu();
            }
        } );

        // On Tab Press Toggle Sub Menu ( Enter Press )
        $( '.js-ct-dropdown-toggle' ).on( 'keydown', function( e ) {
            var keyCode = e.keyCode || e.which;
            if (keyCode == 13) {
                e.preventDefault();
                $( this ).toggleClass( 'toggled' );
                $( this ).next().slideToggle();
            }
        } );

        $( '.menubar-right' ).on( 'click', show_menu );
        $( '.mobile-menu-overlay' ).on( 'click', hide_menu );
        $( '.menubar-close' ).on( 'click', hide_menu );

        $( '.menubar-right, .menubar-close' ).on( 'click', function( e ){
            e.preventDefault();
        } );
    } );

    /**
    * Sticky Header
    */
    $( window ).on( 'load resize', function() {
        var header              = $( '.fixed-header' );
        var header_container    = $( '.header-container' );
        if( $( header )[0] ) {
            var header_height   = header[0].getBoundingClientRect().height;
            var header_c_height = header_container[0].getBoundingClientRect().height;
            var sticky          = 'sticky-header';
            var no_sticky       = 'no-stick';
            var topbar          = $( '.top-bar' );
            var topbar_height   = topbar.height();
            var adjust_height   = $( '.fixed-spacing' );

            var trans_header    = $( '.ct-transparent-logo>img' );
            var trans_logo      = trans_header.data('transparent-logo');
            var main_logo       = trans_header.data('main-logo');

            var logo_container  = $( '.logo-container' );
            var lc_height       = logo_container.height();

            var adminbar_height = 0;
            var fixed_boxed     = '';

            // If Logged In
            if( $( document ).find( '#wpadminbar' ) ) {
                if ( $(window).width() > 768 ) {
                    adminbar_height = $( '#wpadminbar' ).height();
                }
            }

            // If Boxed Layout
            if ( $( 'body' ).hasClass( 'box-layout' ) ) {
                fixed_boxed = 'fixed-boxed';
            }

            // If Topbar Enabled
            if ( !$( '.top-bar' ).is( ':visible' ) && !$( document ).find( logo_container ) ) {
                header.addClass( sticky + ' ' + fixed_boxed );
                adjust_height.css( 'margin-bottom', header_height );
            }

            // If Small device remove sticky and boxed layout
            if ( $(window).width() < 768 ) {
                logo_container.removeClass( sticky + ' ' + fixed_boxed ).css( 'top', 'unset' );
            }

            $( window ).scroll( function() {
                // If centerd header
                if( $( logo_container )[0] ) {

                    if( $( this ).scrollTop() > ( topbar_height + lc_height ) ) {
                        header.addClass( sticky + ' ' + fixed_boxed ).css( 'top', adminbar_height );
                        adjust_height.css( 'margin-bottom', header_height );
                        header.removeClass( no_sticky );

                        // Replace main logo with transparent logo
                        $( trans_header ).attr( 'src', main_logo );
                    } else {
                        header.removeClass( sticky + ' ' + fixed_boxed ).css( 'top', 0 );
                        adjust_height.css( 'margin-bottom', 0 );
                        header.addClass( no_sticky );

                        // Replace transparent logo with main logo
                        $( trans_header ).attr( 'src', trans_logo );
                    }

                    // If small device and in centered header
                    if ( $( window ).width() < 768 ) {
                        if ( $( '.menu-container' ).hasClass( 'sticky-header' ) ) {
                            logo_container.addClass( sticky + ' ' + fixed_boxed ).css( 'top', adminbar_height );
                            adjust_height.css( 'margin-bottom', header_c_height-1 );
                            header.removeClass( no_sticky );

                            // Replace main logo with transparent logo
                            $( trans_header ).attr( 'src', main_logo );
                        } else {
                            logo_container.removeClass( sticky + ' ' + fixed_boxed ).css( 'top', 'unset' );
                            adjust_height.css( 'margin-bottom', 0 );
                            header.addClass( no_sticky );

                            // Replace transparent logo with main logo
                            $( trans_header ).attr( 'src', trans_logo );
                        }
                    }
                } else {
                    // Normal Header not centered
                    if ( $( this ).scrollTop() > topbar_height ) {
                        header.addClass( sticky + ' ' + fixed_boxed ).css( 'top', adminbar_height );
                        adjust_height.css( 'margin-bottom', header_height );
                        header.removeClass( no_sticky );

                        // Replace main logo with transparent logo
                        $( trans_header ).attr( 'src', main_logo );
                    } else {
                        header.removeClass( sticky + ' ' + fixed_boxed ).css( 'top', 0 );
                        adjust_height.css( 'margin-bottom', 0 );
                        header.addClass( no_sticky );

                        // Replace transparent logo with main logo
                        $( trans_header ).attr( 'src', trans_logo );
                    }
                }
            } );
        }
    } );

    /**
     * Back to Top
     */

     $( '#back-to-top' ).on( 'click', function( e ){
        e.preventDefault();
        $( "html, body" ).animate( {scrollTop: 0}, 300 );
     } );

     $( window ).scroll( function() {
        if ( $( this ).scrollTop() > 800 ) {
            $( '#back-to-top' ).fadeIn();
        } else {
            $( '#back-to-top' ).fadeOut();
        }
    } );

    /**
     * Search Icon Switch
     */
    var $search_icon        =   $( '.search-icon' );

    $search_icon.on( 'click', function( e ) {
        var $search_dropdown    =   $( this ).next( '.search-dropdown' );

        if ( $search_dropdown.hasClass( 'search-hidden' ) || $search_dropdown.hasClass( 'search-default' ) ) {

            $search_dropdown.attr( 'class', 'search-dropdown search-shown' );

        } else if( $search_dropdown.hasClass( 'search-shown' ) ) {

            $search_dropdown.attr( 'class', 'search-dropdown search-hidden' );

        }
    } );


    $('.share-icons a').on('click', function(e){
        e.preventDefault();
        window.open(this.href,'targetWindow','scrollbars=yes,resizable=yes,width=700,height=500')
    });

    /**
     * 3.0 - Masonry Layout
    */

    if ( jQuery().masonry ) {
        var $grid = $( '.ct-grid' ).masonry( {
            // options
            itemSelector: '.grid-item'
        } );

        // layout Masonry after each image loads
        $grid.imagesLoaded().progress( function() {
            $grid.masonry( 'layout' );
        });
    }

    /**
    * Initiate Offscreen Plugin
    */

    $( '.menu-item-has-children' ).on( 'mouseover', function(){
        var dropdown = $( this ),
            menu = dropdown.find( 'ul' );

        // Adjust if it's off the screen
        if( menu.is( ':off-right' ) ) {
            menu.addClass( 'to-left' );
        }
    } );

    /**
     * 4.0 - Infinite Scroll
     */
    jQuery(document).ready( function(){
        if ( document.querySelector('.load-more-infinite') !== null ) {
            var loading = true;
            $(window).scroll(function() { //detact scroll
                if( loading && $(window).scrollTop() + $(window).height() >= $(document).height()*.8) { //scrolled to bottom of the page
                    loading = false;
                    var that            = $('.load-more-infinite');
                    var page            = that.data('page');
                    var new_page        = page+1;
                    var ajaxurl         = that.data('url');
                    var taxonomy_val    = that.data('taxonomy-val');
                    var taxonomy_type   = that.data('taxonomy-type');
                    var author          = that.data('author');

                    $.ajax( {
                        url     :   ajaxurl,
                        type    :   'post',
                        data    :   {
                            page            :   page,
                            taxonomy_type   :   taxonomy_type,
                            taxonomy_val    :   taxonomy_val,
                            author          :   author,
                            action          :   'apex_business_load_more'
                        },
                        error   :   function( response ) {
                            console.log( response );
                        },
                        success :   function( response ) {

                            if ( response == 0 ) {
                                $( '.spinner' ).removeClass( 'spinner' ).addClass( 'no-posts button' ).html( '<p>No More Post</p>' ).delay(1500).queue(function(next) {
                                        $(this).addClass("hide");
                                        next();
                                    });
                            }

                            that.data( 'page', new_page );
                            var el = jQuery( response );

                            $grid = $( '.ct-grid' );

                            if ( jQuery().masonry ) {
                                $grid.append( el ).imagesLoaded(function(){
                                    $grid.masonry( 'appended', el );
                                });
                            } else {
                                $grid.append( el );
                            }

                            loading = true;
                        },
                    } );

                }
            });
        }
    } );

} )( jQuery );
