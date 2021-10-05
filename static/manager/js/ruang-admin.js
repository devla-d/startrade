(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

// Modal Javascript

$(document).ready(function () {
  		 /* csrf token */
       function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
            }
          }
        }
        return cookieValue;
      }
      const csrftoken = getCookie('csrftoken');
  $("#myBtn").click(function () {
    $('.modal').modal('show');
  });

  $("#modalLong").click(function () {
    $('.modal').modal('show');
  });

  $("#modalScroll").click(function () {
    $('.modal').modal('show');
  });

  $('#modalCenter').click(function () {
    $('.modal').modal('show');
  });


  $('#approveBtn').on('click',function (e) {
		 
		var submit_btn = $(this)
		submit_btn.text('processing...').attr('disabled','disabled')
		$.ajax({
			type: "POST",
			url: "/manager/payments-approve/",
			data: {
				user_id:$("#user_id").val(),
				invest_id : $("#invest_id").val(),
				pop_id : $("#pop_id").val(),
				 csrfmiddlewaretoken: csrftoken,
			},
			
			success: function(data) {
				 $('#msgalert').show().addClass('alert-info').text(`${data.msg}`)
				// window.location.reload();
 
			},
      complete : function () {
        submit_btn.text('Approved')

      }

		});
	 
		
	})

  $('#declineBtn').on('click',function (e) {
		 
		var submit_btn = $(this)
		submit_btn.text('processing...').attr('disabled','disabled')
		$.ajax({
			type: "POST",
			url: "/manager/payments-decline/",
			data: {
				user_id:$("#user_id").val(),
				invest_id : $("#invest_id").val(),
				pop_id : $("#pop_id").val(),
				 csrfmiddlewaretoken: csrftoken,
			},
			
			success: function(data) {
				 $('#msgalert').show().addClass('alert-danger').text(`${data.msg}`)
				// window.location.reload();
 
			},
      complete : function () {
        submit_btn.text('Declined')

      }

		});
	 
		
	})









});

// Popover Javascript

$(function () {
  $('[data-toggle="popover"]').popover()
});
$('.popover-dismiss').popover({
  trigger: 'focus'
});


 