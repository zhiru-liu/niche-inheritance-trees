clear all
% Using collapse data to plot AC vs r_e %
%% set default color order. %matlab only provides 7 colors then it'll repeat
co = [0    0.4470    0.7410;
    0.8500    0.3250    0.0980;
    0.9290    0.6940    0.1250;
    0.4940    0.1840    0.5560;
    0.4660    0.6740    0.1880;
    0.3010    0.7450    0.9330;
    0.6350    0.0780    0.1840;
    0.6471    0.3804    0.0510;
    0.7529    0.7765    0.0824;
    0.8471    0.3882    0.7098   
    ];
set(groot,'defaultAxesColorOrder',co)

%%%%%%%%%%%%%%%%%

r_e = [0.1, 0.05, 0.01, 0.005, 0.001, 0.0005, 0.0001];
eta = 1.51;
threshold = 10^6;
%% plot C(A) versus r_epsilon
% This generates Fig 3

fig1 = figure; 
%fig1.Renderer = 'Painters'; % save as vector graph
set(fig1,'resize','off')
set(fig1,'PaperUnit','inches')
set(fig1,'PaperSize',[3.375 2.5])
set(fig1,'PaperPositionMode','manual')
set(fig1,'PaperPosition',[0 0 3.375 2.5])

hold on
legent_ar = {};
% Plot all the C(A) data
for i = 7:-1:1
    filename = ['../data/data_collapse/AC/AC_average_sigma=25_r_e_',int2str(i-1),'.csv'];
    AC_data = load(filename);
    A = AC_data(:,1);
    C = AC_data(:,2);
    A_ = A(A < threshold);
    C_ = C(A < threshold);
    clear AC_data
    p1 = plot(A_, C_./A_, '.');
    set(p1, 'markersize', 1)
    legend_ar{8-i} = sprintf('$r_{\\epsilon%d}=%0.4f$',i,r_e(i));
end
%%
% Plot the MFT calculations. Only small sigmas bc large ones no longer
% agree
%  AA = sort(A_);
%  for i = 1:4
%      p3 = plot(AA, MFT(AA, std(i))./AA,'-');
%      set(p3, 'linewidth', 1)
%      legend_ar{6+i} = sprintf('MF $\\sigma_%d=%1.1f$',i,std(i));
%  end
% 
% % And reference line
% p2 = plot( A_, exp( log(A_) * eta )./A_ );
% set(p2, 'linewidth', 1, 'color', 'r')
%%
hold off
box on
set(gca, 'xscale', 'log');
set(gca, 'yscale', 'log');
%ylabel('$\bar{C}/A$', 'interpreter', 'latex')
%xlabel('$A$', 'interpreter', 'latex') 
ylim([10^0 10^3])
xlim([10^0 10^6])
set(gca, 'XTick', (10.^(0:6)));
set(gca, 'YTick', (10.^(0:3)));
set(gca, 'fontsize', 12)
%leg = legend(legend_ar, 'Interpreter', 'latex');
%set(leg, 'fontsize', 5, 'location', 'northwest')
%legend boxoff
% Call the helper function to adjust marker size
%legendmarkeradjust(5)

filename = '../plotting/results/AC_r_e_inset';
%print(filename,'-dpdf');
%print(filename, '-dpng', '-r600')
%}