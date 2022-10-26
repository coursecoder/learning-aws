var LEADERBOARD = (function () {

	var expose = {

	}, hide = {
		formatWithUnderscores: formatWithUnderscores,
		handleGetAllGamers: handleGetAllGamers,
		loadAllItems: loadAllItems,
		loadItemsByTag: loadItemsByTag,
		printItems: printItems,
		setUpHandlers: setUpHandlers,
		showAll: showAll,
		showTopGamer: showTopGamer,
		toggleDescription: toggleDescription

	};

	(function init() {
		setUpHandlers();
		showTopGamer();
	})();

	function formatWithUnderscores(str) {
		return str.replace(/ /g, "_");
	}
	function handleGetAllGamers(a, b, c) {
		// debugger; //todo
		printItems("todo");
	}

	function loadAllItems() {
		$("[data-role='browse_leaderboard_content'] > section").remove();
		if (window.LEADERBOARD_CONFIG.API_GW_BASE_URL_STR === null) {
			$.get("all_gamers.json", printItems);
		} else {
			$.get(window.LEADERBOARD_CONFIG.API_GW_BASE_URL_STR + "/leaderboard", printItems);
		}
	}

	function loadItemsByTag() {
		$("[data-role='browse_leaderboard_content'] > section").remove();
		var tag_name_str = "top_gamer";
		if (window.LEADERBOARD_CONFIG.API_GW_BASE_URL_STR === null) {
			$.get("all_gamers.json", printItems);
		} else {
			$.get(window.LEADERBOARD_CONFIG.API_GW_BASE_URL_STR + "/leaderboard/" + tag_name_str, printItems);
		}
	}

	function printItems(response) {
		var html_str = '';
		html_str += '<section class="flex-grid">';
		if (response.leaderboard_item_arr) {
			for (var i_int = 0, o = {}; i_int < response.leaderboard_item_arr.length; i_int += 1) {
				o = response.leaderboard_item_arr[i_int];

				html_str += '<div data-gamer_id="' + o.gamer_id_str + '">';



				html_str += '<h3>';
				html_str += o.gamer_name_str;
				html_str += '</h3>';
				html_str += '<h4>' + (o.score_int) + '</h4>';
				html_str += '<section>';
				html_str += '<span>';
				html_str += o.rank_int;
				html_str += '</span>';
				html_str += '</section>';
				html_str += '<img src="images/items/' + formatWithUnderscores(o.gamer_name_str) + '.svg" alt="Image for ' + o.gamer_name_str + '" />';
				html_str += '</div>';
			}
		}
		html_str += '</section>';
		$("[data-role='toast']").text("");
		$("[data-role='browse_leaderboard_content']")
			.append(html_str);
	}

	function setUpHandlers() {
		$(document).on("click", "[data-action='show_all'][data-selected='not_selected']", showAll);
		$(document).on("click", "[data-action='show_top_gamer'][data-selected='not_selected']", showTopGamer);
		$(document).on("click", "[data-action='show_description']", toggleDescription);
	}

	function showAll() {
		$("[data-role='toast']").text("Loading all players...");
		$("[data-action='show_all']").attr("data-selected", "selected");
		$("[data-action='show_top_gamer']").attr("data-selected", "not_selected");
		loadAllItems();
	}

	function showTopGamer() {
		$("[data-role='toast']").text("Loading leaderboard...");
		$("[data-action='show_all']").attr("data-selected", "not_selected");
		$("[data-action='show_top_gamer']").attr("data-selected", "selected");
		loadItemsByTag();
	}

	function toggleDescription() {
		var $card_el = $(this)
			.parent()
			.parent();
		if ($card_el.attr("data-showing-description") === "showing") {
			$card_el.attr("data-showing-description", "not_showing");
		} else {
			$card_el.attr("data-showing-description", "showing");
		}
	}

	return expose;

})();