Vim的插件：
Vundle（管理插件）
YouCompleteMe (自动补全)
NERDTree (文件资源管理器)
Vim-jinja2-Syntax (jinja2语法)
## 下载Vundle
在账户根目录下
```
git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

## 配置.vimrc文件（在账户根目录下新建），文件内容如下：
```
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" let Vundle manage Vundle, required
Plugin 'VundleVim/Vundle.vim'
" color
Bundle 'tomasr/molokai'
" syntax and language improvements
Bundle 'Glench/Vim-Jinja2-Syntax'
" auto complete
Bundle 'Valloric/YouCompleteMe'
" source tree
" Bundle 'scrooloose/nerdtree'
" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
"  Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
"  Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
"  Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
"  Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line
" *******************************************************
" vim setting
" *******************************************************
set t_Co=256
syntax on
colorscheme molokai
set shortmess=atI
set showcmd
set autoindent
set cindent
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set smarttab
set number
set cursorline
set history=1000
set hlsearch
set incsearch
set langmenu=zh_CNUTF-8
set helplang=cn
set cmdheight=2
set mouse=a
" NERDTree setting
" open a NERDTree automatically when wim starts up
" autocmd vimenter * NERDTree

" close vim if the only window left open is a NERDTree
" autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType ==primary") | q | endif

set completeopt-=preview
let g:ycm_add_preview_to_completeopt = 0
"for YouCompleteMe

```
保存退出：wq

## 安装插件
```
 vim  (进入vim,会报错是正常的。)
 :PluginInstall  （执行命令）
```




set nocompatible      
filetype off               
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
Plugin 'VundleVim/Vundle.vim'
Bundle 'tomasr/molokai'
Bundle 'Glench/Vim-Jinja2-Syntax'
Bundle 'Valloric/YouCompleteMe'
call vundle#end()            " required
filetype plugin indent on    " required
set t_Co=256
syntax on
colorscheme molokai
set shortmess=atI
set showcmd
set autoindent
set cindent
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
set smarttab
set number
set cursorline
set history=1000
set hlsearch
set incsearch
set langmenu=zh_CNUTF-8
set helplang=cn
set cmdheight=2
set mouse=a
set completeopt-=preview
let g:ycm_add_preview_to_completeopt = 0










