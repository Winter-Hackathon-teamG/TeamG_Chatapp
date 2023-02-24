// 親要素の取得
const chatHeader = document.getElementById('chat-header');

// 子要素の数に応じた高さを計算する関数
function calculateHeaderHeight() {
  const childCount = chatHeader.childElementCount;
  const headerHeight = 50 + (childCount * 10); // この計算式は適宜変更する
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