# OSIx > Modules > Username

This Module Enables the Username Discovery over +150 WebSites and Detailed Information from Some Specific Ones.

### Specific WebSites with Extended Informations
  * **GitHub** - Name, Nickname, Bio, Location, Account ID, Profile Pictures, Repositories, Followers and Following
  * **Twitch** - PENDING
  * **Tumblr** - PENDING
  * **Pinterest** - PENDING
  * **Steam** - Steam ID's (ID3, ID64, Default ID), Username, Full Name, Location, Profile Picture, Profile State and Profile Creation Date)
  * **Pastebin** - Username, Views Count, All Pastes Views Count, Profile Picture and all Public Pastes
  * **Gravatar** - Username, FullName, Gravatar ID, Location, Profile Picture and Public Links

### Complete Command Line
```bash
python3 -m OSIx --username guibacellar \
                --username_scan \
                --username_allow_nsfw_scan \
                --username_print_result --username_show_all \
                --username_enable_dump_file
``` 

### Basic Command Line

```bash
python3 -m OSIx --username USERNAME
``` 
 * **--username** - Target Username
 
### Username Scan over Internet

Scan the Target Username over +150 WebSites.
```bash
python3 -m OSIx --username USERNAME --username_scan
``` 

### Username Scan over Internet + NSFW Sites
Scan the Target Username over +150 WebSites + NSFW Ones.
```bash
python3 -m OSIx --username USERNAME --username_scan --username_allow_nsfw_scan
``` 

### Print Scan Result (Only Founded Entries)

Print on Sysout the Websites where the Username was Found.

```bash
python3 -m OSIx --username USERNAME --username_allow_nsfw_scan --username_print_result
``` 

### Print Scan Result (All Entries)

Print on Sysout all Entries (Founded and Not Founded).

```bash
python3 -m OSIx --username USERNAME --username_allow_nsfw_scan --username_print_result --username_show_all
``` 

### Dump Output File

Exports a CSV File with all Entries at 'data/export/username_USERNAME.csv'.

```bash
python3 -m OSIx --username USERNAME --username_allow_nsfw_scan --username_enable_dump_file
``` 

---
### Example Utilization
```bash
python3 -m OSIx --username marcos \
               --username_scan --username_allow_nsfw_scan \
               --username_print_result --username_enable_dump_file
```

**OUTPUT**
```bash
[*] Loading Configurations:
[*] Installed Modules:
	bitcoin_wallet.py
	bitcoin_wallet_graph.py
	github_username_data_digger.py
	http_navigation_manager.py
	input_args_handler.py
	state_file_handler.py
	temp_file_manager.py
	username_handler.py
[*] Executing Pipeline:
	[+] input_args_handler.InputArgsHandler
		job_name = 19C914BDEE3346DDA4F281E536F70E5B
		purge_temp_files = False
		btc_wallet = 
		btc_get_transactions = 
		export_btc_transactions_as_graphml = False
		export_btc_transactions_as_gephi = True
		username = marcos
		username_scan = True
		username_allow_nsfw_scan = True
		username_print_result = True
		username_show_all = False
		username_enable_dump_file = True
	[+] temp_file_manager.TempFileManager
 		Checking Age data/temp/state for 31557600 seconds
 		Checking Age data/temp/bitcoin_wallet for 604800 seconds
 		Checking Age data/temp/username_search for 604800 seconds
	[+] state_file_handler.LoadStateFileHandler
	[+] http_navigation_manager.HttpNavigationManagerHandler
	[+] bitcoin_wallet.BitcoinWalletInfoDownloader
		Target BTC Wallet Empty.
	[+] bitcoin_wallet.BitcoinWalletTransactionsDownloader
	[+] bitcoin_wallet_graph.BitcoinWalletGraphGenerator
		Target BTC Wallet Empty.
	[+] username_handler.UsernameScanner
		NSFW Sites Allowed.
		Starting Scan with 20 Workers.
		7Cups: Claimed > https://www.7cups.com/@marcos
		9GAG: Claimed > https://www.9gag.com/u/marcos
		About.me: Claimed > https://about.me/marcos
		Rate Your Music: Claimed > https://rateyourmusic.com/~marcos
		Redbubble: Claimed > https://www.redbubble.com/people/marcos
		Reddit: Claimed > https://www.reddit.com/user/marcos
		Repl.it: Claimed > https://repl.it/@marcos
		ReverbNation: Claimed > https://www.reverbnation.com/marcos
		Roblox: Claimed > https://www.roblox.com/user.aspx?username=marcos
		OnlyFans: Claimed > https://onlyfans.com/marcos
	[+] github_username_data_digger.GithubUsernameDataDigger
		Full Name.......: Marcos Supressed Name for GitHub Documentation
		Nick Name.......: Marcos
		Bio.............: None
		Location........: Florianópolis
		WebSite.........: None
		Account ID......: 181829
		Profile Picture.: https://avatars.githubusercontent.com/u/181829?v=4
		Repos...........: 10
			marcos.github.io (None) at https://github.com/Marcos/marcos.github.io
			add-ui (None) at https://github.com/Marcos/add-ui
			marc-os (Scripts to help me!) at https://github.com/Marcos/marc-os
			add-api (None) at https://github.com/Marcos/add-api
			redisdemo (None) at https://github.com/Marcos/redisdemo
			productApp (None) at https://github.com/Marcos/productApp
			appleOrchard (None) at https://github.com/Marcos/appleOrchard
			dt-job-processor (None) at https://github.com/Marcos/dt-job-processor
			newsreader (None) at https://github.com/Marcos/newsreader
			tdc-2015-sample-projects (Examples of Java EE 7 projects using Maven) at https://github.com/Marcos/tdc-2015-sample-projects
		Followers.......: 50
			marcelbraghini (Marcel Braghini) at https://github.com/marcelbraghini
			KevinSotomayor (Kevin S.) at https://github.com/KevinSotomayor
			MalletJorge (Jorge Mallet) at https://github.com/MalletJorge
			ledbruno (Bruno Ledesma) at https://github.com/ledbruno
			t-bonatti (Tiago Bonatti) at https://github.com/t-bonatti
			rafaelvanat (Rafael Maciel Vanat) at https://github.com/rafaelvanat
			prafaelo (Pablo Si) at https://github.com/prafaelo
			dmonti (Daniel Monti) at https://github.com/dmonti
			rafaelcamargo (Rafael Camargo) at https://github.com/rafaelcamargo
			caarlos0 (Carlos Alexandro Becker) at https://github.com/caarlos0
		Following.......: 50
			GoesToEleven (Todd McLeod) at https://github.com/GoesToEleven
			michaelmcguirk (Michael McGuirk) at https://github.com/michaelmcguirk
			robertoduessmann (Roberto Duessmann) at https://github.com/robertoduessmann
			nilemarbarcelos (Nilemar de Barcelos) at https://github.com/nilemarbarcelos
			ledbruno (Bruno Ledesma) at https://github.com/ledbruno
			davicdsalves (Davi Alves) at https://github.com/davicdsalves
			yanaga (Edson Yanaga) at https://github.com/yanaga
			B0go (Victor Bogo) at https://github.com/B0go
			dariopinheiro (Dário Braz Pinheiro Junior) at https://github.com/dariopinheiro
			fernahh (Fernando Rodrigues) at https://github.com/fernahh
			luizm (Luiz Muller) at https://github.com/luizm
			tmatias (Tiago Matias) at https://github.com/tmatias
			merencia (Lucas Merencia) at https://github.com/merencia
			raduq (Raduan Silva dos Santos) at https://github.com/raduq
			dmonti (Daniel Monti) at https://github.com/dmonti
			lapavila (Luiz Ávila) at https://github.com/lapavila
			deividi (Deividi) at https://github.com/deividi
        [+] steam_username_data_digger.SteamUsernameDataDigger
            Running...
        [+] steam_username_data_digger.SteamIdFinderDataDigger
            Running...
        [+] steam_username_data_digger.SteamDataPrinter
            Steam Id..............: STEAM_0:0:288072
            Steam Id 3............: [U:1:576144]
            Steam Id 64 Hex.......: 11000010008ca90
            Steam Id.64 Dec.......: 76561197960841872
            Username..............: _AgainstAllOdds_
            Full Name.............: Marcus Supressed Here
            Location..............: Kaufbeuren, Bayern, Germany
            Profile Picture.......: https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/avatars/ac/acdab7c604bf1e502fa8ae79d004d0b7298eec69_full.jpg
            Profile State.........: Public
            Profile Creation Date.: September 16th, 2003
	[+] state_file_handler.SaveStateFileHandler
```

 [<< BACK](../README.md)