const deleteButton = document.getElementById("channel-delete");
const deleteChannelModal = document.getElementById("delete-channel-modal");
const deletePageButtonClose = document.getElementById("delete-page-close-btn");
const deleteChannelConfirmBtn = document.querySelector("#delete-channel-confirmation-btn");

const deleteChannel = () => {
  if (uid !== channel.uid) {
    return;
  } else {
    modalOpen("delete");
  }
};
deleteButton.addEventListener("click", deleteChannel);

deletePageButtonClose.addEventListener("click", () => {
  modalClose("delete");
});

// 削除確認モーダルでの削除実行コード
const confirmationButtonLink = document.getElementById("delete-confirm-link"); // id取得（aタグ）
const url = `/delete/${channel.id}`; // urlを作成
confirmationButtonLink.setAttribute("href", url); // urlを取得id（aタグ）のhref属性に設定
