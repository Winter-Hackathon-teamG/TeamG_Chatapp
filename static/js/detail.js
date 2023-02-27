// 親要素の取得
const chatHeader = document.getElementById('header-tag-list');

// タグの表示数に応じたヘッダー高さを計算する関数
function calculateHeaderHeight() {
  const chatHeader = document.getElementById('header-tag-list');
  const tagCount = chatHeader.childElementCount; // タグの表示数取得
  const headerWidth = chatHeader.offsetWidth; // ヘッダーの幅取得
  const tagWidth = chatHeader.firstElementChild.offsetWidth; // タグの幅取得
  const tagHeight = 120; // 一行あたりのタグ表示の高さを設定
  const maxTagPerRow = Math.floor(headerWidth / tagWidth); // 各行に表示できるタグの最大数
  const rowCount = Math.ceil(tagCount / maxTagPerRow); // タグ表示の行数
  const headerHeight = rowCount * tagHeight; // ヘッダー高さ
  return headerHeight;
}

// スクロール時にヘッダーの高さを更新する関数
function updateHeaderHeight() {
  chatHeader.style.height = calculateHeaderHeight() + 'px';
}

// 初期化時にヘッダーの高さを設定する
updateHeaderHeight();

// スクロール時にヘッダーの高さを更新する
window.addEventListener('scroll', updateHeaderHeight);

// スクロール時だけでなく、タグ一覧が表示される度にヘッダーの高さを更新する
function showHeader() {
  chatHeader.style.display = 'block';
  updateHeaderHeight();
}

function hideHeader() {
  chatHeader.style.display = 'none';
}

// ウィンドウサイズが変更されたときにもヘッダーの高さを更新する
window.addEventListener('resize', function() {
  if (chatHeader.style.display === 'block') {
    updateHeaderHeight();
  }
});

/*
// タグ一覧のアコーディオンメニュー化
document.addEventListener('DOMContentLoaded', function() {
  const list = document.getElementById('header-tag-list');
  list.style.display = 'none'; // 初期状態で非表示にする
  const title = document.querySelector('.tag-accordion-title');
  title.addEventListener('click', function() {
    if (list.style.display === 'none') {
      showHeader();
    } else {
      hideHeader();
    }
  });
});
*/
