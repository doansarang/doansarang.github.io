// 도안사랑교회 홈페이지 스크립트: 모바일 메뉴, 앨범 사진 크게 보기
(function () {
  var body = document.body;

  // 모바일 메뉴 열고 닫기
  var openBtn = document.querySelector('.m-menu-btn');
  var closeBtn = document.querySelector('.m-close');
  var dim = document.querySelector('.m-dim');
  function setMenu(open) { body.classList.toggle('menu-open', open); }
  if (openBtn) openBtn.addEventListener('click', function () { setMenu(true); });
  if (closeBtn) closeBtn.addEventListener('click', function () { setMenu(false); });
  if (dim) dim.addEventListener('click', function () { setMenu(false); });
  document.querySelectorAll('.m-toggle').forEach(function (btn) {
    btn.addEventListener('click', function () { btn.parentElement.classList.toggle('open'); });
  });

  // 앨범 사진 크게 보기
  var photos = Array.prototype.slice.call(document.querySelectorAll('.photos .photo'));
  if (!photos.length) return;
  var idx = 0;
  var box = document.createElement('div');
  box.className = 'lightbox';
  box.hidden = true;
  box.innerHTML = '<span class="lb-count"></span><img alt=""><button class="lb-prev" aria-label="이전 사진">&#8249;</button>' +
    '<button class="lb-next" aria-label="다음 사진">&#8250;</button><button class="lb-close" aria-label="닫기">&times;</button>';
  body.appendChild(box);
  var img = box.querySelector('img');
  var count = box.querySelector('.lb-count');

  function show(i) {
    idx = (i + photos.length) % photos.length;
    img.src = photos[idx].getAttribute('href');
    count.textContent = (idx + 1) + ' / ' + photos.length;
    box.hidden = false;
    box.style.display = '';
  }
  function hide() { box.hidden = true; box.style.display = 'none'; }
  hide();

  photos.forEach(function (a, i) {
    a.addEventListener('click', function (e) { e.preventDefault(); show(i); });
  });
  box.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
  box.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
  box.querySelector('.lb-close').addEventListener('click', hide);
  box.addEventListener('click', function (e) { if (e.target === box) hide(); });
  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'Escape') hide();
    if (e.key === 'ArrowLeft') show(idx - 1);
    if (e.key === 'ArrowRight') show(idx + 1);
  });

  // 손가락으로 넘기기
  var startX = null;
  box.addEventListener('touchstart', function (e) { startX = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (startX === null) return;
    var dx = e.changedTouches[0].clientX - startX;
    if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
    startX = null;
  });
})();
