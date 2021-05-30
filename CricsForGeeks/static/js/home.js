///// Section-1 CSS-Slider /////    
  // Auto Switching Images for CSS-Slider
  function bannerSwitcher() {
    next = $('.sec-1-input').filter(':checked').next('.sec-1-input');
    if (next.length) next.prop('checked', true);
    else $('.sec-1-input').first().prop('checked', true);
  }

  var bannerTimer = setInterval(bannerSwitcher, 5000);
  function scrollprevent() {
        $('html').css({
          'overflow-y': 'hidden',
          'height': '100%'
    })
  }
  function scrollrestore()
  {
        $('html').css({
      'overflow-y': 'auto',
      'height': 'auto'
    })
  }
  $('nav .controls label').click(function() {
    clearInterval(bannerTimer);
    bannerTimer = setInterval(bannerSwitcher, 5000)
  });
   scrollprevent();
   $(window).on("load",function(){    
          setTimeout(function(){$(".loading-wrapper").fadeOut("slow");
          scrollrestore();
          console.log('jae');       
        },1000);
        
    });
// set the time here
///// Anchor Smooth Scroll /////
//   $('.main-menu a, .learn-more-button a').click(function(e){
    
//     e.preventDefault();
        
//     var target = $(this).attr('href');
        
//     $('html, body').animate({scrollTop: $(target).offset().top}, 1000);
//     return false;
//   });