function toDo(message) {
  alert(message);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
function clearCookies() {
  // 获取所有 cookies
  var cookies = document.cookie.split(";");

  // 循环遍历并清除每一个 cookie
  for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i];
      var eqPos = cookie.indexOf("=");
      var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
      document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
  }

  // 清除后的提示
  alert("所有 cookies 已清除！");
}

function initUpdateAddress() {
  $(".add_city").change(function () {
    updateTowns($(this));
  });
}
function updateTowns(citySelect) {
  var city = citySelect.val(); // 获取选中的城市

  var townSelect = citySelect.closest('form').find('.add_town'); // 根据表单查找相应的城镇下拉菜单

  if (city) {
    $.ajax({
      url: loadTownsUrl,
      data: {
        city: city, // 将城市作为参数发送
      },
      success: function (data) {
        townSelect.empty(); // 清空现有的选项
        townSelect.append($("<option>").val("").text("---------")); // 添加默认选项

        $.each(data, function (index, item) {
          townSelect.append($("<option>").val(item.tac_town).text(item.tac_town));
        });
      },
    });
  }
}
