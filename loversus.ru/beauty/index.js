'use strict';

var complData = [
      'You look great today.',
      'You\'re a smart cookie.',
      'I bet you make babies smile.',
      'I like your style.',
      'I appreciate you.',
      'You are the most perfect you there is.',
      'You are enough.',
      'You\'re strong.',
      'You\'re an awesome friend.',
      'You deserve a hug right now.',
      'You\'re more helpful than you realize.',
      'You\'ve got all the right moves!',
      'You\'re all that and a super-size bag of chips.',
      'You are brave.',
      'You have the courage of your convictions.',
      'You are making a difference.',
      'You\'re a great listener.',
      'I bet you sweat glitter.',
      'That color is perfect on you.',
      'Hanging out with you is always a blast.',
      'You always know — and say — exactly what I need to hear when I need to hear it.',
      'You smell really good.',
      'When you say, "I meant to do that," I totally believe you.',
      'You\'re more fun than a ball pit filled with candy. (And seriously, what could be more fun than that?)',
      'You\'re wonderful.',
      'You have cute elbows. For reals!',
      'Your bellybutton is kind of adorable.',
      'Your hair looks stunning.',
      'You\'re one of a kind!',
      'You should be thanked more often. So thank you!!',
      'You always know how to find that silver lining.',
      'You always know just what to say.',
      'If someone based an Internet meme on you, it would have impeccable grammar.',
      'You could survive a Zombie apocalypse.',
      'You\'re more fun than bubble wrap.',
      'When you make a mistake, you fix it.',
      'You\'re great at figuring stuff out.',
      'Your voice is magnificent.',
      'You\'re so thoughtful.',
      'Your creative potential seems limitless.',
      'You\'re gorgeous — and that\'s the least interesting thing about you, too.',
      'Somehow you make time stop and fly at the same time.',
      'You seem to really know who you are.',
      'Babies and small animals probably love you.',
      'If you were a scented candle they\'d call it Perfectly Imperfect (and it would smell like summer).',
      'How do you keep being so funny and making everyone laugh?',
      'Has anyone ever told you that you have great posture?',
  ];

var set_compliment = function set_compliment() {
    var ind = Math.floor(Math.random() * complData.length);
    $('.box__inner-heading').text(complData[ind]);
};

$(document).ready(function () {

  var $btnOuter = $('.box__btn--outer');
  var $btnInner = $('.box__btn--inner');
  var $inner = $('.box__inner');
  var $outer = $('.box__outer');
  var $logo = $('.box__outer-logo');
  var slideOutInnerDelay = 650;
  var animation = false;
  var numOfHeartsBg = 50; // Change this variable also in CSS
  var numOfHeartsInner = 25; // Change this variable also in CSS

  set_compliment();

  $(document).on('click', '.box__btn--outer', function () {
    if (animation) return;
    animation = true;
    $inner.addClass('show-in-inner');
    $outer.addClass('show-out-outer');

    setTimeout(function () {
      $btnOuter.removeClass('scale-in-btn-outer');
      $logo.removeClass('beat-logo');
      animation = false;
    }, 750);
  });

  $(document).on('click', '.box__btn--inner', function () {
    if (animation) return;
    $inner.removeClass('show-in-inner').addClass('slide-out-inner');
    $outer.removeClass('show-out-outer');

    setTimeout(function () {
      $inner.removeClass('slide-out-inner');
      $btnOuter.addClass('scale-in-btn-outer');
      $logo.addClass('beat-logo');
      animation = false;
      set_compliment();
    }, slideOutInnerDelay);

  });

  //*** Hearts ***

  var hearts = function hearts() {
    var docFragBg = $(document.createDocumentFragment());
    var docFragInner = $(document.createDocumentFragment());
    var $con = $('.container');
    var $conInnerHearts = $('.box__inner-hearts');

    for (var i = 1, l = 1; i <= numOfHeartsBg, l <= numOfHeartsInner; i++, l++) {
      var heartBg = $('<div class="heart heart-bg-' + i + '">\n    <i class="fa fa-heart" aria-hidden="true"></i>\n  </div>');
      var heartInner = $('<div class="heart heart-inner-' + l + '">\n    <i class="fa fa-heart fa-heart--inner" aria-hidden="true"></i>\n  </div>');
      docFragBg.append(heartBg);
      docFragInner.append(heartInner);
    }

    $con.append(docFragBg);
    $conInnerHearts.append(docFragInner);
  };
  hearts();

  if ($(window).width() < 768) {
      $('.box__inner-heading').css('font-size', '1.5em');
  }
});
