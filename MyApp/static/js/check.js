$(function () {

	var delete_list = new Array();

	// 全选
	$('#checkAll').click(function () {
		if (this.checked == true) {
			delete_list = [];
			$('input[name="selectFlag"]:checkbox').each(function () {
				this.checked = true;
				delete_list.push($(this).next().text());
				// console.log(delete_list);
			});
		} else {
			$('input[name="selectFlag"]:checkbox').each(function () {
				this.checked = false;
				delete_list = [];
				// console.log(delete_list);
			});
		}
	});

	// 单选
	$('input[name="selectFlag"]:checkbox').click(function () {
		var bundle_id = $(this).next().text();
		if (this.checked == true) {
			// console.log(bundle_id);
			delete_list.push(bundle_id);
			// console.log(delete_list);
		} else {
			// console.log(bundle_id);
			delete_list.splice(delete_list.indexOf(bundle_id),1);
			// console.log(delete_list);
		}
	});

	//Alertify JS
	reset = function () {
		$("#toggleCSS").href = "/static/css/alertify.core.css";
		alertify.set({
		  	labels: {
		    ok: "确认",
		    cancel: "取消"
	  		},
		delay: 2500,
		buttonReverse: false,
		buttonFocus: "ok"
		});
	};

	// 删除全部确认
	$('#deleteAll').click(function () {
	    reset();
	    alertify.confirm("请确认删除所选模型", function (e) {
	      if (e) {
	      	deleteBundles();
	        alertify.success("删除成功!");
	      } else {
	        alertify.error("取消操作!");
	      }
	    });
	    return false;
  	});

  	// 删除单个确认
  	$('.deleteOne').click(function () {
  		var url = $(this).attr("href");
  		reset();
  		alertify.confirm("请确认删除该模型", function (e) {
	      if (e) {
	      	deleteBundle(url);
	        alertify.success("删除成功!");
	      } else {
	        alertify.error("取消操作!");
	      }
	    });
	    return false;
  	});

  	// 删除单个
  	function deleteBundle(url) {
  		console.log(url);
  		window.location.href = url;
  	}

  	// 删除全部
  	function deleteBundles() {
  		var url = "delete.html?bundles_id=";
  		url = url + delete_list.join("&bundles_id=");
  		// console.log(url);
  		window.location.href = url;
  	}
});