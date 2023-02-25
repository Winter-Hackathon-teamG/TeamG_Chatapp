// 親要素の取得
const chatHeader = document.getElementById('header-tag-list');

// タグの表示数に応じたヘッダー高さを計算する関数
function calculateHeaderHeight() {
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