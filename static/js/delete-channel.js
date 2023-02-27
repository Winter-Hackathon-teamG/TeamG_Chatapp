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
