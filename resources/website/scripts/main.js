var MAIN = (function () {

	var expose = {

	}, hide = {
		attemptLogin: attemptLogin,
		establishAPIGWStatus: establishAPIGWStatus,
		establishAndHandleCognitoStatus: establishAndHandleCognitoStatus,
		setUpHandlers: setUpHandlers,
		showCreateReportBtn: showCreateReportBtn,
		handleReportCreationSuccess: handleReportCreationSuccess,
		handleReportCreationError: handleReportCreationError

	};

	function attemptLogin() {
		if (window.LEADERBOARD_CONFIG.COGNITO_LOGIN_BASE_URL_STR !== null) {
			window.location = window.LEADERBOARD_CONFIG.COGNITO_LOGIN_BASE_URL_STR;
		} else {
			alert("Integration with Cognito coming soon!");
		}
	}



	function establishAPIGWStatus() {
		if (window.LEADERBOARD_CONFIG.API_GW_BASE_URL_STR !== null) {
			console.log("You are now using API GW to get game data");
		} else {
			console.log("Ok we will use hard coded product data from `all_gamers.json`");
		}
	}

	function showCreateReportBtn() {
		var html_str = '';
		var $target = $("[data-action='attempt_login']");
		html_str += '<aside data-action="attempt_create_report">report</aside>';
		$(html_str).insertAfter($target);
		$target.hide();
	}

	function establishAndHandleCognitoStatus() {
		if (window.LEADERBOARD_CONFIG.COGNITO_LOGIN_BASE_URL_STR !== null) {
			console.log("You are using Cognito for logins. How cool!");
			$(document).on("click", "[data-role='login_button']", function () {
				location.href = window.LEADERBOARD_CONFIG.COGNITO_LOGIN_BASE_URL_STR;
			});
			if (localStorage.getItem("bearer_str") !== null) {
				console.log("We have a token to use");
				showCreateReportBtn();
			}
		} else {
			console.log("Cognito has not been set up yet");
			$(document).on("click", "[data-role='login_button']", function () {
				alert("I Have No POST API to call!");
			});
		}
	}

	function attemptCreateReport(ce) {
		if (window.LEADERBOARD_CONFIG.API_GW_BASE_URL_STR === null) {
			showProblem("I have no POST API to call!");
			return;
		}
		//have to be logged in 
		var token_str_or_null = localStorage.getItem("bearer_str");

		if (token_str_or_null === null) {
			return showProblem("You need to be logged in to save your score to the leaderboard");
		}

		// showWorking();
		//construct bearer token  in the headerTODO
		//use $.ajax to get error handling too
		$.ajax({
			url: window.LEADERBOARD_CONFIG.API_GW_BASE_URL_STR + "/" + "create_report",
			method: "POST",
			data: {},
			headers: {
				"Authorization": "Bearer " + token_str_or_null
			},
			error: handleReportCreationError,
			success: handleReportCreationSuccess
		});
	}

	function handleReportCreationSuccess(response) {
		console.info(response);
		//shoudl have message str (ok)
		if (response.message_str) {
			showProblem(response.message_str);
		} else {
			if (response.executionArn) {
				showProblem("Your score is being added, please check the Leaderboard");
			} else {
				showProblem(JSON.parse(response).message_str);
			}
		}
	}

	function handleReportCreationError(response) {
		console.error(response);
		showProblem("Something went wrong");
	}

	function showProblem(msg_str) {
		alert(msg_str);
	}

	(function init() {
		console.log("Ok lets get started");
		setTimeout(function () {
			$(".main_image").addClass("loaded");
		}, 1000);
		establishAPIGWStatus();
		establishAndHandleCognitoStatus();
		setUpHandlers();

	})();

	function setUpHandlers() {
		$(document).on("click", "[data-action='attempt_login']", attemptLogin);
		$(document).on("click", "[data-action='attempt_create_report']", attemptCreateReport);
	}



	return expose;

})();