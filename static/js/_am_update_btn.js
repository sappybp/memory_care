function Check1(){
    var checked = confirm("本当に更新しますか？");
    if (checked == true) {
        return true;
    } else {
        return false;
    }
}
function Check2(){
    var checked = confirm("本当に削除しますか？");
    if (checked == true) {
        return true;
    } else {
        return false;
    }
}