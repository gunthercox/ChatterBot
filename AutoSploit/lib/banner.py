import os
import random

VERSION = "4.0"


def banner_1(line_sep="#--", space=" " * 30):
    banner = """\033[1m\033[36m{space_sep}_____     _       _____     _     _ _
{sep1}Author : Vector/NullArray |  _  |_ _| |_ ___|   __|___| |___|_| |_
{sep1}Twitter: @Real__Vector    |     | | |  _| . |__   | . | | . | |  _|
{sep1}Type   : Mass Exploiter   |__|__|___|_| |___|_____|  _|_|___|_|_|
{sep1}Version: {v_num}{spacer}                              |_|
##############################################\033[0m
    """.format(sep1=line_sep, v_num=VERSION, space_sep=space, spacer=" " * 8)
    return banner


def banner_2():
    banner = r"""
{blue}--+{end} {red}Graffiti the world with exploits{end} {blue}+--{end}
{blue}--+{end}             __   ____            {blue}+--{end} 
{blue}--+{end}            / _\ / ___)           {blue}+--{end}
{blue}--+{end}           /    \\___ \           {blue}+--{end}
{blue}--+{end}           \_/\_/(____/           {blue}+--{end}
{blue}--+{end}            {red}AutoSploit{end}            {blue}+--{end}
{blue}--+{end}           NullArray/Eku          {blue}+--{end}
{blue}--+{end}{minor_space2}             v({red}{vnum}{end}){minor_space}             {blue}+--{end}
    """.format(vnum=VERSION, blue="\033[36m", red="\033[31m", end="\033[0m",
               minor_space=" " * 1 if len(VERSION) == 3 else "",
               minor_space2=" " * 1 if len(VERSION) == 3 else "")
    return banner


def banner_3():
    banner = r'''#SploitaSaurusRex{green}
                                           O_  RAWR!!
                                          /  > 
                                        -  >  ^\
                                      /   >  ^ /   
                                    (O)  >  ^ /   / / /  
       _____                        |            \\|//
      /  __ \                      _/      /     / _/
     /  /  | |                    /       /     / /
   _/  |___/ /                   /      ------_/ / 
 ==_|  \____/                 _/       /  ______/
     \   \                 __/           |\
      |   \_          ____/              / \      _                    
       \    \________/                  |\  \----/_V
        \_                              / \_______ V
          \__                /       \ /          V
             \               \        \
              \______         \_       \
                     \__________\_      \ 
                        /    /    \_    | 
                       |   _/       \   |
                      /  _/          \  |
                     |  /            |  |
                     \  \__          |   \__
                     /\____=\       /\_____=\{end} v({vnum})'''''.format(
        green="\033[1m\033[32m", end="\033[0m", vnum=VERSION
    )
    return banner


def banner_4():
    banner = r"""
{red}    .__.    ,     __.   .     , 	{end}
{red}    [__]. .-+- _ (__ ._ | _ *-+-	{end}
{red}    |  |(_| | (_).__)[_)|(_)| | 	{end}
{red}                     |          	{end}
{red}          _ ._  _ , _ ._		{end}
{red}         (_ ' ( `  )_  .__)	{end}
{red}       ( (  (    )   `)  ) _)	{end}
{red}      (__ (_   (_ . _) _) ,__)	{end}
{red}          `~~`\ ' . /`~~`		{end}
{red}               ;   ;		{end}
{red}               /   \		{end}
{red} _____________/_ __ \_____________ {end}

{blue}--------The Nuclear Option--------{end}
{blue}-----+       v({red}{vnum}{end}{blue}){spacer}+-----{end}
{blue}-----------NullArray/Eku----------{end}	  
{blue}__________________________________{end}
    """.format(vnum=VERSION, blue="\033[36m", red="\033[31m", end="\033[0m",
               spacer=" " * 9 if len(VERSION) == 3 else " " * 7)
    return banner


def banner_5():
    banner = r"""
                  {red}. '  .{end}
               {red}' .( '.) '{end}
       {white}_{end}     {red}('-.)' (`'.) '{end}
      {white}|0|{end}{red}- -(  #autosploit  ){end}
   {grey}.--{end}{white}`+'{end}{grey}--.{end}  {red}.  (' -,).(') .{end}
   {grey}|`-----'|{end}   {red}(' .) - ('. ){end}
   {grey}|       |{end}    {red}. (' `.  ){end}
   {grey}|  {red}.-.{end}  {grey}|{end}       {red}` .  `{end}
   {grey}| {red}(0.0){end}{grey} |{end}
   {grey}| {red}>|=|<{end} {grey}|{end}
   {grey}|  {red}`"`{end}{grey}  |{end}
   {grey}|       |{end}
   {grey}|       |{end}
   {grey}`-.___.-'{end}
   v({red}{version}{end})
    """.format(end="\033[0m", grey="\033[36m", white="\033[37m", version=VERSION, red="\033[31m")
    return banner


def banner_main():
    """
    grab a random banner each run
    """
    banners = [
        banner_5, banner_4,
        banner_3, banner_2, banner_1
    ]
    if os.getenv("Graffiti", False):
        return banner_5()
    elif os.getenv("AutosploitOG", False):
        return banner_1()
    elif os.getenv("Nuclear", False):
        return banner_4()
    elif os.getenv("SploitaSaurusRex", False):
        return banner_3()
    elif os.getenv("Autosploit2", False):
        return banner_2()
    else:
        return random.choice(banners)()
