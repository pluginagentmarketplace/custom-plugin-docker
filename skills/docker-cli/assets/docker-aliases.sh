# Docker CLI Aliases
# Add to ~/.bashrc or ~/.zshrc

alias d='docker'
alias dc='docker compose'
alias dps='docker ps'
alias dpsa='docker ps -a'
alias di='docker images'
alias drm='docker rm'
alias drmi='docker rmi'
alias dlog='docker logs -f'
alias dex='docker exec -it'
alias dprune='docker system prune -af'
alias dstop='docker stop $(docker ps -q)'
alias dclean='docker rm $(docker ps -aq)'
