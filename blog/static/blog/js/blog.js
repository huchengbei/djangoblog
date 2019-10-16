(function($) {
  "use strict"; // Start of use strict

  // auto dropdown
  $(".dropdown-toggle").on('mouseover',
      function(){$(this).dropdown('toggle')});
  $(".dropdown-menu").on('mouseout',
      function(){$(this).parent().children('.dropdown-toggle').dropdown('toggle')});
  $.scrollUp({
    scrollName: "scrollUp",
    topDistance: "300",
    topSpeed: 300,
    animation: "fade",
    animationInSpeed: 200,
    animationOutSpeed: 200,
    scrollText: '<div class="mt-2"><i class="fa fa-arrow-up"></i></div>',
    activeOverlay: !1
  });

})(jQuery);