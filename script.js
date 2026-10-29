// Вкажіть постійне запрошення Discord, наприклад https://discord.gg/your-server
const DISCORD_INVITE = 'https://discord.com/invite/mzwFcDHk5Z';

const translations = {
  uk: {
    navModes:'Режими',navCommunity:'Спільнота',navJoin:'Приєднатися',
    heroEyebrow:'PS5 · CALL OF DUTY · СПІЛЬНОТА',heroTitle:'ЗНАЙДИ<br>СВОЇХ <em>У ГРІ.</em>',
    heroText:'Шукаєш, з ким пограти в Call of Duty на PS5? Знаходь команду для Modern Warfare 4, DMZ і Warzone в нашому Discord.',
    joinDiscord:'Приєднатися до Discord',viewModes:'Дивитися режими',heroCaption:'ОДНА КОМАНДА. ТРИ РЕЖИМИ.',
    introTitle:'МАТЧ ПОЧИНАЄТЬСЯ<br><em>З КОМАНДИ.</em>',
    introText:'Потрібні тімейти для Call of Duty на PS5? У GameWar можна знайти гравців, зайти в голосовий канал Discord і зібрати загін для наступного матчу.',
    modesTitle:'ОБИРАЙ РЕЖИМ',modesIntro:'Три напрямки для гри. Один Discord для всіх.',
    multiplayer:'МУЛЬТИПЛЕЄР',multiplayerText:'Шукаєш команду для мультиплеєра Modern Warfare 4? Заходь у Discord і збирай паті на матч.',
    dmzText:'Знайди напарників для DMZ: місії, голосовий зв’язок і вихід із зони разом.',
    warzoneText:'Потрібен сквад у Warzone на PS5? Знаходь тімейтів і грай з командою.',
    futureTitle:'ГРА ЗМІНИТЬСЯ.<br><em>ЗАГІН ЗАЛИШИТЬСЯ.</em>',
    futureText:'Граємо в Modern Warfare 4 і разом переходимо в майбутні частини Call of Duty.',
    joinTitle:'ТВОЄ МІСЦЕ<br><em>В ЗАГОНІ.</em>',joinText:'Готовий до наступного матчу? Заходь на сервер і знайомся з командою.',
    footerText:'Спільнота гравців PS5 · Call of Duty',
    dialogTitle:'ПОСИЛАННЯ ЩЕ НЕ ДОДАНО',dialogText:'Додайте запрошення Discord у файл script.js, щоб кнопки відкривали сервер.',dialogOk:'Зрозуміло'
  },
  ru: {
    navModes:'Режимы',navCommunity:'Сообщество',navJoin:'Присоединиться',
    heroEyebrow:'PS5 · CALL OF DUTY · СООБЩЕСТВО',heroTitle:'НАЙДИ<br>СВОИХ <em>В ИГРЕ.</em>',
    heroText:'Ищешь, с кем поиграть в Call of Duty на PS5? Найди команду для Modern Warfare 4, DMZ и Warzone в нашем Discord.',
    joinDiscord:'Присоединиться к Discord',viewModes:'Смотреть режимы',heroCaption:'ОДНА КОМАНДА. ТРИ РЕЖИМА.',
    introTitle:'МАТЧ НАЧИНАЕТСЯ<br><em>С КОМАНДЫ.</em>',
    introText:'Нужны тиммейты для Call of Duty на PS5? В GameWar можно найти игроков, зайти в голосовой канал Discord и собрать отряд для следующего матча.',
    modesTitle:'ВЫБИРАЙ РЕЖИМ',modesIntro:'Три направления для игры. Один Discord для всех.',
    multiplayer:'МУЛЬТИПЛЕЕР',multiplayerText:'Ищешь команду для мультиплеера Modern Warfare 4? Заходи в Discord и собирай пати на матч.',
    dmzText:'Найди напарников для DMZ: задания, голосовая связь и выход из зоны вместе.',
    warzoneText:'Нужен сквад в Warzone на PS5? Находи тиммейтов и играй с командой.',
    futureTitle:'ИГРА ИЗМЕНИТСЯ.<br><em>ОТРЯД ОСТАНЕТСЯ.</em>',
    futureText:'Играем в Modern Warfare 4 и вместе переходим в будущие части Call of Duty.',
    joinTitle:'ТВОЁ МЕСТО<br><em>В ОТРЯДЕ.</em>',joinText:'Готов к следующему матчу? Заходи на сервер и знакомься с командой.',
    footerText:'Сообщество игроков PS5 · Call of Duty',
    dialogTitle:'ССЫЛКА ЕЩЁ НЕ ДОБАВЛЕНА',dialogText:'Добавьте приглашение Discord в файл script.js, чтобы кнопки открывали сервер.',dialogOk:'Понятно'
  }
};

document.querySelectorAll('[data-lang]').forEach(button => button.addEventListener('click', () => {
  const selected = button.dataset.lang;
  const current = document.documentElement.lang;
  if (selected === current) return;
  const path = location.pathname;
  const base = path.endsWith('/ru/') || path.endsWith('/ru/index.html')
    ? path.replace(/ru\/(index\.html)?$/, '')
    : path.replace(/index\.html$/, '');
  location.href = selected === 'ru' ? base + 'ru/index.html' : base + 'index.html';
}));
document.querySelector('#year').textContent = new Date().getFullYear();

const dialog = document.querySelector('#invite-dialog');
document.querySelectorAll('.discord-link').forEach(link => {
  if (DISCORD_INVITE) {
    link.href = DISCORD_INVITE;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
  } else {
    link.addEventListener('click', event => { event.preventDefault(); dialog.showModal(); });
  }
});
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
document.querySelector('.dialog-ok').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });

const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('.nav');
menu.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
});
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('open');
  menu.setAttribute('aria-expanded', 'false');
}));

