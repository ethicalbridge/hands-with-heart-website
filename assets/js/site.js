/* Hands With Heart — navigation, filters and contact form. No dependencies. */
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }
  document.querySelectorAll('.sub-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var li = btn.parentElement;
      var open = li.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      document.querySelectorAll('.has-sub.open').forEach(function (li) { li.classList.remove('open'); });
      if (nav) nav.classList.remove('open');
      if (toggle) toggle.setAttribute('aria-expanded', 'false');
    }
  });

  // Generic filter buttons: <div class="filter" data-target="#id"> <button data-filter="x">
  document.querySelectorAll('.filter').forEach(function (bar) {
    var target = document.querySelector(bar.getAttribute('data-target'));
    if (!target) return;
    bar.querySelectorAll('button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        bar.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        btn.setAttribute('aria-pressed', 'true');
        var f = btn.getAttribute('data-filter');
        target.querySelectorAll('[data-cat]').forEach(function (el) {
          el.hidden = !(f === 'all' || el.getAttribute('data-cat').split(' ').indexOf(f) > -1);
        });
      });
    });
  });

  // Contact form: opens the visitor's email client with the message filled in.
  var form = document.getElementById('contact-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(form);
      var subject = '[' + d.get('topic') + '] Message from ' + d.get('name');
      var body = d.get('message') + '\n\n— ' + d.get('name') + ' (' + d.get('email') + ')';
      window.location.href = 'mailto:' + form.getAttribute('data-to') +
        '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    });
  }
})();
