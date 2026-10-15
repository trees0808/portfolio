(function () {
  // mobile nav
  var t = document.querySelector('.nav-toggle');
  var ul = document.querySelector('.nav ul');
  if (t && ul) t.addEventListener('click', function () { ul.classList.toggle('open'); });

  // highlight current nav link
  var path = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav li a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === path || (path === 'index.html' && href.indexOf('index.html') === 0 && href.indexOf('#') < 0)) a.classList.add('active');
  });

  // hide images that haven't been added yet (placeholders for old-project galleries)
  document.querySelectorAll('img[data-optional]').forEach(function (img) {
    img.addEventListener('error', function () {
      var f = img.closest('figure') || img;
      f.style.display = 'none';
      var g = img.closest('.gallery');
      if (g && !g.querySelector('img:not([style*="display: none"])') && g.children.length && [].every.call(g.children, function (c) { return c.style.display === 'none'; })) {
        g.insertAdjacentHTML('afterend', '<p class="muted">（项目截图整理中）</p>');
        g.style.display = 'none';
      }
    });
  });

  // play videos only when visible
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) { v.play().catch(function () {}); } else { v.pause(); }
      });
    }, { threshold: 0.25 });
    document.querySelectorAll('video[autoplay]').forEach(function (v) { io.observe(v); });
  }
})();
