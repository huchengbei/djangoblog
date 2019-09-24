(function($) {
  "use strict"; // Start of use strict

  // auto dropdown
  $(".dropdown-toggle").on('mouseover',
      function(){$(this).dropdown('toggle')});
  $(".dropdown-menu").on('mouseout',
      function(){$(this).parent().children('.dropdown-toggle').dropdown('toggle')});

})(jQuery);