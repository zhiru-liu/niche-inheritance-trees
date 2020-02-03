% data
x1 = [];
y1 = [];

x2 = [];
y2 = [];

x3 = [];
y3 = [];

% set default color order. %matlab only provides 7 colors then it'll repeat
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


% set up graph size
fig1 = figure; 
fig1.Renders = 'Painters'; % save as vector graph
set(fig1,'resize','off')
set(fig1,'PaperUnit','inches')
set(fig1,'PaperSize',[3.375 2.5])
set(fig1,'PaperPositionMode','manual')
set(fig1,'PaperPosition',[0 0 3.375 2.5])

% plot
hold on % for multiple plotting
hp1 = plot(x1,y1,'*', x2,y2,'*');  % scatter plot
hp2 = plot(x1,y1, x2,y2);  % line plot, no marker
hold off

% set curve properties
set(hp1,'MarkerSize',2) % set markersize for both curves
set(hp2,'linewidth',1)  % set linewidth for both curves
% or
hp2(1).LineWidth = 1; % set linewidth separately, note the Capital letters.
hp2(2).LineWidth = 2;

hp2(1).Color = [0.3,0.1,0.3];  % matlab automatically assign colors for curves
hp2(2).Color = [0.8,0.8,0];   % use this syntax to change color of a certain curve

% legend
leg1 = legend('$x_1$','y1','x2','$y_2$');  
set(leg1,'interpreter', 'latex','fontsize',6)  % LaTex in the legend/title. 

set(leg1,'location','northeast') % position of the legend
legend boxoff  % boxon by default

%below: legend in columns
ax1 = gca;
leg1 = (ax1, hp1, 'dot1', 'dot2');
set(leg1, 'fontsize', 6)
legend boxoff

ax2 = axes('position',get(gca,'position'),'visible','off'); % now, the gca gives ax2, invisible
leg2 = (ax2, hp2, 'line1', 'line2');
set(leg2, 'fontsize', 6)
legend boxoff

sex(ax1, 'linewidth',1)
xlabel(ax1, 't', 'fontsize', 9) %gca returns ax2 invisible
ylabel(ax1, 'p', 'fontsize', 9)
%above: legend in columns

box on % box at the axes
xlim([0 10])  % set axis limit, useful when having inset
ylim([0 10]) 

%set ticks if needed
ax = gca;
ax.XTick = [1 2 3];
ax.YTick = [1 2 3 5 7];
ax.XTickLabel = {'1.0' '2.0', '3.0'};

set(gca, 'LineWidth', 1)
set(gca, 'fontsize', 8) % don't use font smaller than 6 for publication
xlabel('Generation','fontsize',9);  % write this line after set fontsize of axis ticks
ylabel('Copy number','fontsize',9);  % otherwise, the label fontsize will be over-written

% inset if needed
ins = axes('position',[0.37 0.6 0.28 0.3]); % position of the inset axes, numbers mean proportions
ins = axes('outerposition',[0.37 0.6 0.28 0.3]); % OR, set the outerposition of the inset axes, numbers mean proportions
inp = plot(x3,y3,'*b', 'MarkerSize', 1.5 ); % markersize, linewidth can be specified here since only plotting one curve
set(gca,'linewidth',1,'fontsize',6) % axis of the inset graph
xlabel('LINE copy number','fontsize',7)
ylabel('SINE copy number','fontsize',7)


% subplots if needed
ax1 = subplot(1,2,1);  % This generates two suplots side by side with exactly the same dimension
ax2 = subplot(1,2,2);
set(ax1, 'linewith', 1, 'fontsize', 6);
set(ax2, 'linewith', 1, 'fontsize', 6);
%%% OR set the position of subplots by hand. Do not use 'outerposition',
%%% because something will be rescaled by matlab
set(ax1, 'position', [0.2 0.2 0.2 0.7]);
set(ax2, 'position', [0.7 0.2 0.2 0.7]); % offset the "left" coordinate


% finish and save
filename = '.pdf';
print(filename,'-dpdf')  % use print function, don't save or export the fig window

