clear

mark = 10:5:20;
nrep = 50;
poolobj = gcp('nocreate');
if isempty(poolobj)
    c = parcluster;
    parpool(c);
end
warning off
pctRunOnAll warning off
fprintf('Progress:\n');
fprintf(['\n' repmat('.',1,size(mark,2)) '\n\n']);

parfor s = 1:size(mark,2)
    s;
    [p,q,r] = parfunc2(s,mark,nrep);
    resultsn{s} = p;
    resultsc{s} = q;
    resultsf{s} = r;
    fprintf('\b|\n');
end


%% Unpack

results_store = [];
num = 0;
for i = 1:size(resultsc,2)
    results_storec(:,:,i) = cell2mat(resultsc(i));
    results_storen(:,:,i) = cell2mat(resultsn(i));
    results_storef(:,:,i) = cell2mat(resultsf(i));
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
