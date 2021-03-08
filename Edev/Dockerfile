FROM node:15.9.0-alpine3.12
ARG REPO=gitee
ARG REPO_URL=$REPO.com
ARG JD_SHELL=jd_shell
ARG JD_SHELL_BRANCH=master
ARG JD_SHELL_HOST=jd_shell_$REPO
ARG JD_SHELL_KEY="-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn\nNhAAAAAwEAAQAAAQEAyey3HbpcJtOaTOMZh1lS6aGzJOr4wVgBG5Ba81t7D1aLbHS+rB/o\nxMDPtk3xPCNcw6mOzgM+NX4TbeZkU7g12ejRiYXWX6rY0giTaqKA3NjqvGGXoagTJxK9D5\nxEPka+4qNbs1eKhq4LpeoWIzoDRpSfgDd/yVvKiF3U9Yycxs3v52QtXuC6Q+/p3hxW/5sW\nBgjsb4Wga45/yH7I2MbfH9RDY9Xips9OKxQ3nZFAwbbMfSfZnLm3ifXUZfvnSALAsqyo02\nS6t3Z7nOGNahQrIiGv3ShMj6kOAmEhRQCtM/JfkLhsA631EJ6E6SfRdU2pv0H1omj2UjNN\nkduijcdjCwAAA8AVGCi2FRgotgAAAAdzc2gtcnNhAAABAQDJ7Lcdulwm05pM4xmHWVLpob\nMk6vjBWAEbkFrzW3sPVotsdL6sH+jEwM+2TfE8I1zDqY7OAz41fhNt5mRTuDXZ6NGJhdZf\nqtjSCJNqooDc2Oq8YZehqBMnEr0PnEQ+Rr7io1uzV4qGrgul6hYjOgNGlJ+AN3/JW8qIXd\nT1jJzGze/nZC1e4LpD7+neHFb/mxYGCOxvhaBrjn/IfsjYxt8f1ENj1eKmz04rFDedkUDB\ntsx9J9mcubeJ9dRl++dIAsCyrKjTZLq3dnuc4Y1qFCsiIa/dKEyPqQ4CYSFFAK0z8l+QuG\nwDrfUQnoTpJ9F1Tam/QfWiaPZSM02R26KNx2MLAAAAAwEAAQAAAQEAyA0mymQU4j6oU153\nr1m2xFL4ai4Fb4Ah8M4O3aWXgPWsQjJTqbIfabbg0uvbgUpDoHH/UmlyG4sh8rLcWPlbGN\n4JoqcfYT6he00VyALhimu5/BLwKC+dcgulla6rCcwLV/yiYEbtrksGrUUC07mo/ydF8sCJ\ncNPpDztvPismM+qVcLdWuWE9m5eMx8t3X8riFJaVgms6LbWhJIEmpDXMbm0nZKRDdVRPnN\nq2LbaTFHxYiz77qZ2GjYkPS62Z9DAv1hRDx076F5LlMtWFBjJbLrMILIEuAuNczgZ/5Fe8\nYOC5OXmPIz422jeglCFRGSEMg2IZY7aGiEpawxBEd2VP8QAAAIBprAYBCQexXPlwdMv/Kx\n69HDQ837OfU+tTEVc56Q21KTEq5KSwv0OZaJNIRdbygZd7nCS4ZAkZgUshescBrVGBt6+l\nGTJMaHVlCvf8r2ptI82E1Tt85XgRoPyIJVPMl/UTxAwv6dfHTACnuXe3wl/xwa09Ad/iO8\n7kODEsLqSzgwAAAIEA+EDHB+6ooO5IJ9e3KtG91n+SYacXN7s3zTsbyNV4mCT5tRj49xPo\neKIjYAnZlGmQP9AVoqRN4YuDGSz/oNFXKbGziHXybZFvxFi7fs79D+0yW2jOF/F9gpBauy\nbN54K0T8O/G9FdJTiCp9sX5K95rnhNfRiwI7KtvEQB17SZM3kAAACBANA51XB5avHoVmW9\nO3MUuF83IcayfaY6UQxOEJBnTvPwu/n3X0ydZvZlsfJp7NOVILTKmLHtXW6sZ5X257II8U\nY1IbK03NFO1n8pY+RdNwN7oLw53i4GeHoqquY/KU2Er084JaW0QpH6/hitrX4nF3SfPjKU\nB1iQSpFbj0SdPEWjAAAACHJvb3RAbmFzAQI=\n-----END OPENSSH PRIVATE KEY-----"
ARG JD_SCRIPTS=jd_scripts
ARG JD_SCRIPTS_BRANCH=master
ARG JD_SCRIPTS_HOST=jd_scripts_$REPO
ARG JD_SCRIPTS_KEY="-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABFwAAAAdzc2gtcn\nNhAAAAAwEAAQAAAQEAvRQk2oQqLB01iVnJKrnI3tTfJyEHzc2ULVor4vBrKKWOum4dbTeT\ndNWL5aS+CJso7scJT3BRq5fYVZcz5ra0MLMdQyFL1DdwurmzkhPYbwcNrJrB8abEPJ8ltS\nMoa0X9ecmSepaQFedZOZ2YeT/6AAXY+cc6xcwyuRVQ2ZJ3YIMBrRuVkF6nYwLyBLFegzhu\nJJeU5o53kfpbTCirwK0h9ZsYwbNbXYbWuJHmtl5tEBf2Hz+5eCkigXRq8EhRZlSnXfhPr2\n32VCb1A/gav2/YEaMPSibuBCzqVMVruP5D625XkxMdBdLqLBGWt7bCas7/zH2bf+q3zac4\nLcIFhkC6XwAAA9BjE3IGYxNyBgAAAAdzc2gtcnNhAAABAQC9FCTahCosHTWJWckqucje1N\n8nIQfNzZQtWivi8GsopY66bh1tN5N01YvlpL4ImyjuxwlPcFGrl9hVlzPmtrQwsx1DIUvU\nN3C6ubOSE9hvBw2smsHxpsQ8nyW1IyhrRf15yZJ6lpAV51k5nZh5P/oABdj5xzrFzDK5FV\nDZkndggwGtG5WQXqdjAvIEsV6DOG4kl5TmjneR+ltMKKvArSH1mxjBs1tdhta4kea2Xm0Q\nF/YfP7l4KSKBdGrwSFFmVKdd+E+vbfZUJvUD+Bq/b9gRow9KJu4ELOpUxWu4/kPrbleTEx\n0F0uosEZa3tsJqzv/MfZt/6rfNpzgtwgWGQLpfAAAAAwEAAQAAAQEAnMKZt22CBWcGHuUI\nytqTNmPoy2kwLim2I0+yOQm43k88oUZwMT+1ilUOEoveXgY+DpGIH4twusI+wt+EUVDC3e\nlyZlixpLV+SeFyhrbbZ1nCtYrtJutroRMVUTNf7GhvucwsHGS9+tr+96y4YDZxkBlJBfVu\nvdUJbLfGe0xamvE114QaZdbmKmtkHaMQJOUC6EFJI4JmSNLJTxNAXKIi3TUrS7HnsO3Xfv\nhDHElzSEewIC1smwLahS6zi2uwP1ih4fGpJJbU6FF/jMvHf/yByHDtdcuacuTcU798qT0q\nAaYlgMd9zrLC1OHMgSDcoz9/NQTi2AXGAdo4N+mnxPTHcQAAAIB5XCz1vYVwJ8bKqBelf1\nw7OlN0QDM4AUdHdzTB/mVrpMmAnCKV20fyA441NzQZe/52fMASUgNT1dQbIWCtDU2v1cP6\ncG8uyhJOK+AaFeDJ6NIk//d7o73HNxR+gCCGacleuZSEU6075Or2HVGHWweRYF9hbmDzZb\nCLw6NsYaP2uAAAAIEA3t1BpGHHek4rXNjl6d2pI9Pyp/PCYM43344J+f6Ndg3kX+y03Mgu\n06o33etzyNuDTslyZzcYUQqPMBuycsEb+o5CZPtNh+1klAVE3aDeHZE5N5HrJW3fkD4EZw\nmOUWnRj1RT2TsLwixB21EHVm7fh8Kys1d2ULw54LVmtv4+O3cAAACBANkw7XZaZ/xObHC9\n1PlT6vyWg9qHAmnjixDhqmXnS5Iu8TaKXhbXZFg8gvLgduGxH/sGwSEB5D6sImyY+DW/OF\nbmIVC4hwDUbCsTMsmTTTgyESwmuQ++JCh6f2Ams1vDKbi+nOVyqRvCrAHtlpaqSfv8hkjK\npBBqa/rO5yyYmeJZAAAAFHJvb3RAbmFzLmV2aW5lLnByZXNzAQIDBAUG\n-----END OPENSSH PRIVATE KEY-----"
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    LANG=zh_CN.UTF-8 \
    SHELL=/bin/bash \
    PS1="\u@\h:\w \$ " \
    JD_DIR=/jd \
    ENABLE_HANGUP=true \
    ENABLE_WEB_PANEL=true \
    JD_SHELL_URL=git@$JD_SHELL_HOST:evine/$JD_SHELL.git \
    JD_SCRIPTS_URL=git@$JD_SCRIPTS_HOST:lxk0301/$JD_SCRIPTS.git
WORKDIR $JD_DIR
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk update -f \
    && apk upgrade \
    && apk --no-cache add -f bash \
                             npm \
                             coreutils \
                             git \
                             curl \
                             wget \
                             nano \
                             tzdata \
                             perl \
                             openssh-client \
    && rm -rf /var/cache/apk/* \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && mkdir -p /root/.ssh \
    && echo -e $JD_SHELL_KEY > /root/.ssh/$JD_SHELL \
    && echo -e $JD_SCRIPTS_KEY > /root/.ssh/$JD_SCRIPTS \
    && chmod 600 /root/.ssh/$JD_SHELL /root/.ssh/$JD_SCRIPTS \
    && echo -e "Host $JD_SHELL_HOST\n\tHostname $REPO_URL\n\tIdentityFile=/root/.ssh/$JD_SHELL\n\nHost $JD_SCRIPTS_HOST\n\tHostname $REPO_URL\n\tIdentityFile=/root/.ssh/$JD_SCRIPTS" > /root/.ssh/config \
    && chmod 644 /root/.ssh/config \
    && ssh-keyscan $REPO_URL > /root/.ssh/known_hosts \
    && git clone -b $JD_SHELL_BRANCH $JD_SHELL_URL $JD_DIR \
    && cd $JD_DIR/panel \
    && npm install \
    && git clone -b $JD_SCRIPTS_BRANCH $JD_SCRIPTS_URL $JD_DIR/scripts \
    && cd $JD_DIR/scripts \
    && npm install \
    && npm install -g pm2 \
    && ln -sf $JD_DIR/jd.sh /usr/local/bin/jd \
    && ln -sf $JD_DIR/jd.sh /usr/local/bin/task \
    && ln -sf $JD_DIR/git_pull.sh /usr/local/bin/git_pull \
    && ln -sf $JD_DIR/git_pull.sh /usr/local/bin/update \
    && ln -sf $JD_DIR/rm_log.sh /usr/local/bin/rm_log \
    && ln -sf $JD_DIR/rm_log.sh /usr/local/bin/rmlog \
    && ln -sf $JD_DIR/export_sharecodes.sh /usr/local/bin/export_sharecodes \
    && ln -sf $JD_DIR/export_sharecodes.sh /usr/local/bin/codes \
    && ln -sf $JD_DIR/csv.sh /usr/local/bin/csv \
    && cp -f $JD_DIR/docker/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh \
    && chmod 777 /usr/local/bin/docker-entrypoint.sh \
    && chmod 777 $JD_DIR/*.sh \
    && rm -rf /root/.npm
ENTRYPOINT ["docker-entrypoint.sh"]