function _mycomplete_()
{
    local cmd="${1##*/}"
    local word=${COMP_WORDS[COMP_CWORD]}
    local line=${COMP_LINE}
    local values=''

    case "$line" in
        *build-and-run*)

            if [ "${line: -1}" == '-' ]
            then
                values='--skip-tests'
            else
                local elements=()
                local value=''
                local x=`pwd`;
                while [ "$x" != "/" ] ;
                do
                    for i in $(find "$x" -maxdepth 1 -name pom.xml)
                    do
                        local modules=`cat $i | grep '<module>' | sed 's/<module>//' | sed 's/<.*//' | sed 's/ //g' | sed 's/ //g'`
                        elements=(${elements[@]} $modules)

                        if [ `cat $i | grep plugin.dirs | wc -l` -ne "0" ]
                        then
                            local plugin_dirs=`cat $i | sed 's/<project.*>/<project>/' | xmllint --xpath "//plugin.dirs/text()" - | sed 's/^[  ]*//' | sed '/^$/d' | sed 's/,$//' | sed 's/.*\///'`
                            elements=(${elements[@]} $plugin_dirs)
                        fi
                    done
                    x=`dirname "$x"`;
                done

                local sorted=$(printf '%s\n' "${elements[@]}"|sort)
                values=$sorted

            fi
            ;;
        *build-and-run-all*)
            values=''
            ;;
        *core-checkout*)
            values=''
            ;;
        *create*)
            values='project plugin'
            ;;
        *database*)
            values='connect backup restore-latest'
            ;;
        *diffmerge*)
            values=''
            ;;
        *move-theme-to-top-level*)
            values=''
            ;;
        *run-tabs*)
            values=''
            ;;
        *overlay*)
            values=''
            ;;
        *setup-false*)
            values=''
            ;;
        *soy-escape*)
            values=''
            ;;
        *upgrade-analyzer*)
            values=''
            ;;
        *vpn*)
            values='all split my-current-gateway'
            ;;
        *)
            values='build-and-run create database diffmerge move-theme-to-top-level  overlay run-tabs upgrade-analyzer vpn'
    esac

    

    COMPREPLY=($(compgen -W "$values" -- "${word}"))

}

complete -F _mycomplete_ jiver




