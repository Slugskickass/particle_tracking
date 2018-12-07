clear
% resultsna = [];
% resultsca = [];
% resultsfa = [];
% mark = [repmat(0,[1,29]),1:0.5:100];
mark = 30:2:90;
fprintf('Progress:\n');
fprintf(['\n' repmat('.',1,29) '\n\n']);
parfor s = 1:29
    s;
    [p,q,r] = parfunc2(s,mark);
    resultsn{s} = p;
    resultsc{s} = q;
    resultsf{s} = r;
    fprintf('\b|\n');

    %mark = mark+1;
end

%%
mc = [];
errorc = [];
mn = [];
errorn = [];
for i = 1:size(resultsc,3)
    i
    mc(i) = mean([resultsc(:,3,i);resultsc(:,5,i)]);
    errorc(i) = std([resultsc(:,3,i);resultsc(:,5,i)]);
    mn(i) = mean([resultsn(:,3,i);resultsn(:,5,i)]);
    errorn(i) = std([resultsn(:,3,i);resultsn(:,5,i)]);
end

errorbar(mc,errorc)
hold on
errorbar(mn,errorn)
