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

                        local plugin_dirs=`cat $i | sed 's/<project.*>/<project>/' | xmllint --xpath "//plugin.dirs/text()" - | sed 's/^[  ]*//' | sed '/^$/d' | sed 's/,$//' | sed 's/.*\///'`
                        elements=(${elements[@]} $plugin_dirs)
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
            values='project plugin app'
            ;;
        *database*)
            values='connect backup restore-latest'
            ;;
        *run-tabs*)
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
            values='build-and-run core-checkout create database run-tabs setup-false soy-escape upgrade-analyzer vpn'
    esac

    

    COMPREPLY=($(compgen -W "$values" -- "${word}"))

}

complete -F _mycomplete_ jiver




