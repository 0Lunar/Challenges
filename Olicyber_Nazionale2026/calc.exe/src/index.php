<?php

function validate($input)
{
	$matches = [];

	$is_valid = preg_match_all('/^(?:[\s\d+*\/-]|(?:pow\(([^()]*),([^()]*)\))|(?:sqrt\((.*)\)))+$/U', $input, $matches);

	if (!$is_valid) {
		return false;
	}

	// the first match is always the entire string, we don't care
	array_shift($matches);

	foreach ($matches as $m) {
		foreach ($m as $item) {
			if ($item) {
				if (!validate($item)) {
					return false;
				}
			}
		}
	}

	return true;
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>calc.exe</title>
	<link rel="stylesheet" href="https://unpkg.com/7.css">


	<style>
		body {
			background-image: url('/background.jpg');
			background-repeat: no-repeat;
			background-size: cover;
			background-position: center;
			display: flex;
			justify-content: center;
			align-items: center;
			min-height: 100svh;
			padding: 0;
			border: 0;
			margin: 0;
		}

		.bg-credits {
			position: fixed;
			right: 0;
			bottom: 0;
			background: white;
			border-top-left-radius: 4px;
			padding: .12rem .25rem;
		}

		ul[role=menubar]>[role=menuitem] {
			padding-block: 3px;
		}

		.calc-buttons {
			display: grid;
			grid-template-columns: repeat(5, 1fr);
			grid-template-rows: repeat(6, 1fr);
			gap: 6px;
			padding: 10px;
		}

		.calc-buttons button {
			min-width: 0;
			padding: 6px 4px;
		}

		#result {
			margin: 10px;
			margin-bottom: 0;
			padding: 5px;
			padding-top: 26px;
			resize: none;
			background: linear-gradient(#d4dbeeaa, #d4dbee30, #ffffff00);
			border-color: #afafaf;
			box-shadow: inset 0 0 0 1px #fff;
			border-radius: 2px;
			border-style: solid;
			border-width: 1px;
			color: black;
			font-family: monospace;
			font-size: 1.5rem;
			text-align: right;
			min-height: 33px;

			overflow: hidden;
			white-space: nowrap;

			width: 260px;
		}
	</style>
</head>

<body>
	<div class="window active">
		<div class="title-bar">
			<div class="title-bar-text">Calculator</div>
			<div class="title-bar-controls">
				<button aria-label="Minimize"></button>
				<button aria-label="Maximize" disabled></button>
				<button aria-label="Close"></button>
			</div>
		</div>
		<form method="POST" class="window-body">
			<ul role="menubar" class="can-hover">
				<li role="menuitem" tabindex="0" aria-haspopup="true">
					View
					<ul role="menu">
						<li role="menuitem">
							<a href="#menubar">
								Open <span>Ctrl+O</span>
							</a>
						</li>
						<li role="menuitem">
							<a href="#menubar">
								Save <span>Ctrl+S</span>
							</a>
						</li>
						<li role="menuitem" class="has-divider">
							<a href="#menubar">
								Save As... <span>Ctrl+Shift+S</span>
							</a>
						</li>
						<li role="menuitem"><a href="#menubar">Exit</a></li>
					</ul>
				</li>
				<li role="menuitem" tabindex="0" aria-haspopup="true">
					Edit
					<ul role="menu">
						<li role="menuitem"><a href="#menubar">Undo</a></li>
						<li role="menuitem"><a href="#menubar">Copy</a></li>
						<li role="menuitem"><a href="#menubar">Cut</a></li>
						<li role="menuitem" class="has-divider"><a href="#menubar">Paste</a></li>
						<li role="menuitem"><a href="#menubar">Delete</a></li>
						<li role="menuitem"><a href="#menubar">Find...</a></li>
						<li role="menuitem"><a href="#menubar">Replace...</a></li>
						<li role="menuitem"><a href="#menubar">Go to...</a></li>
					</ul>
				</li>
				<li role="menuitem" tabindex="0" aria-haspopup="true">
					Help
					<ul role="menu">
						<li role="menuitem"><a href="#menubar">View Help</a></li>
						<li role="menuitem"><a href="#menubar">About</a></li>
					</ul>
				</li>
			</ul>
			<input id="result" name="input" />
			<div class="calc-buttons">
				<button type="button">MC</button>
				<button type="button" class="mrbtn">MR</button>
				<button type="button">MS</button>
				<button type="button">M+</button>
				<button type="button">M-</button>
				<button type="button">CE</button>
				<button type="button">C</button>
				<button type="button" class="simplebtn">(</button>
				<button type="button" class="simplebtn">)</button>
				<button type="button" class="simplebtn">,</button>
				<button type="button" class="simplebtn">7</button>
				<button type="button" class="simplebtn">8</button>
				<button type="button" class="simplebtn">9</button>
				<button type="button" class="simplebtn">/</button>
				<button type="button" class="sqrtbtn">√</button>
				<button type="button" class="simplebtn">4</button>
				<button type="button" class="simplebtn">5</button>
				<button type="button" class="simplebtn">6</button>
				<button type="button" class="simplebtn">*</button>
				<button type="button" class="powbtn">^</button>
				<button type="button" class="simplebtn">1</button>
				<button type="button" class="simplebtn">2</button>
				<button type="button" class="simplebtn">3</button>
				<button type="button" class="simplebtn">-</button>
				<button type="submit" class="resultbtn" style="grid-column-start: 5; grid-column-end: 6; grid-row-start: 5; grid-row-end: 7;">=</button>
				<button type="button" class="simplebtn" style="grid-column-start: 1; grid-column-end: 3;">0</button>
				<button type="button" class="simplebtn">.</button>
				<button type="button" class="simplebtn">+</button>
			</div>
		</form>
	</div>

	<script>
		<?php
		if (!isset($_POST['input'])) {
		?>
			let input = '';
		<?php
		} else if (validate($_POST['input'])) {
		?>
			let input = '<?php eval('echo ' . $_POST['input'] . ';'); ?>';
		<?php
		} else {
		?>
			let input = 'nope';
		<?php
		}
		?>
		result.value = input;
		input = '';

		document.querySelectorAll('.simplebtn').forEach((btn) => {
			btn.onclick = (e) => {
				input += e.target.innerText;
				result.value = input;
			}
		})

		document.querySelector('.sqrtbtn').onclick = (e) => {
			input += 'sqrt(';
			result.value = input;
		}

		document.querySelector('.powbtn').onclick = (e) => {
			input += 'pow(';
			result.value = input;
		}

		document.querySelector('.mrbtn').onclick = (e) => {
			input += '96';
			result.value = input;
		}
	</script>

	<div class="bg-credits">Image credits: <a href="https://www.freepik.com/free-photo/green-grass-hill-blue-sky_3533637.htm#fromView=keyword&page=1&position=0&uuid=b4c9b19e-4c89-445e-826e-82eb7790dcd1&query=Grass+hill" target="_blank" rel="noopener noreferer">Freepik</a></div>
</body>

</html>