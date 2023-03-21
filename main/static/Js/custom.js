
$(document).ready(function()
{
	"use strict";

	/* 

	1. Vars and Inits

	*/

	var map;
	var header = $('.header');
	var menu = $('.menu');
	var menuActive = false;

	setHeader();

	$(window).on('resize', function()
	{
		setHeader();
	});

	$(document).on('scroll', function()
	{
		setHeader();
	});

	initMenu();
	initSearch();
	initGallery();
	initGoogleMap();

	/* 

	2. Set Header

	*/

	function setHeader()
	{
		if($(window).scrollTop() > 91)
		{
			header.addClass('scrolled');
		}
		else
		{
			header.removeClass('scrolled');
		}
	}

	/* 

	3. Init Menu

	*/

	function initMenu()
	{
		if($('.hamburger').length && $('.menu').length)
		{
			var hamb = $('.hamburger');

			hamb.on('click', function()
			{
				if(!menuActive)
				{
					openMenu();
				}
				else
				{
					closeMenu();
				}
			});
		}
	}

	function openMenu()
	{
		menu.addClass('active');
		menuActive = true;
	}

	function closeMenu()
	{
		menu.removeClass('active');
		menuActive = false;
	}

	/* 

	4. Init Search

	*/

	function initSearch()
	{
		if($('.search_dropdown').length)
		{
			var dds = $('.search_dropdown');
			dds.each(function()
			{
				var dd = $(this);
				if(dd.find('ul > li').length)
				{
					var ddItems = dd.find('ul > li');
					dd.on('click', function()
					{
						dd.toggleClass('active');
					});
					ddItems.each(function()
					{
						var ddItem = $(this);
						ddItem.on('click', function()
						{
							dd.find('span').text(ddItem.text());
						});
					});
				}	
			});
		}
	}

	/* 

	5. Init Gallery

	*/

	function initGallery()
	{
		if($('.gallery_slider').length)
		{
			var gallerySlider = $('.gallery_slider');
			gallerySlider.owlCarousel(
			{
				items:5,
				autoplay:false,
				loop:true,
				nav:false,
				dots:false,
				smartSpeed:1200,
				margin:15,
				responsive:
				{
					0:
					{
						items:1
					},
					576:
					{
						items:2
					},
					768:
					{
						items:3
					},
					992:
					{
						items:4
					},
					1440:
					{
						items:5
					}
				}
			});
		}

		if($('.gallery_item').length)
		{
			$('.colorbox').colorbox(
			{
				rel:'colorbox',
				photo: true,
				maxWidth:'95%',
				maxHeight:'95%'
			});
		}
	}

	/* 

	6. Init Google Map

	*/

	function initGoogleMap()
	{
		var myLatlng = new google.maps.LatLng(34.063685,-118.272936);
    	var mapOptions = 
    	{
    		center: myLatlng,
	       	zoom: 14,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
			draggable: true,
			scrollwheel: false,
			zoomControl: true,
			zoomControlOptions:
			{
				position: google.maps.ControlPosition.RIGHT_CENTER
			},
			mapTypeControl: false,
			scaleControl: false,
			streetViewControl: false,
			rotateControl: false,
			fullscreenControl: true,
			styles:
			[
			  {
			    "featureType": "road.highway",
			    "elementType": "geometry.fill",
			    "stylers": [
			      {
			        "color": "#ffeba1"
			      }
			    ]
			  }
			]
    	}

    	// Initialize a map with options
    	map = new google.maps.Map(document.getElementById('map'), mapOptions);

		// Re-center map after window resize
		google.maps.event.addDomListener(window, 'resize', function()
		{
			setTimeout(function()
			{
				google.maps.event.trigger(map, "resize");
				map.setCenter(myLatlng);
			}, 1400);
		});
	}

});