'use strict';

const filterButtons = [...document.querySelectorAll('.filter-button')];
const courseCards = [...document.querySelectorAll('.course-card')];
const searchInput = document.getElementById('course-search');
const emptyState = document.getElementById('empty-state');
const courseDialog = document.getElementById('course-dialog');
const dialogTitle = document.getElementById('dialog-title');
const dialogDescription = document.getElementById('dialog-description');
const dialogClose = document.getElementById('dialog-close');
const dialogDone = document.getElementById('dialog-done');
const toast = document.getElementById('toast');

let activeCategory = 'all';
let toastTimeout;

function applyCourseFilters() {
  const query = searchInput.value.trim().toLowerCase();
  let visibleCount = 0;

  courseCards.forEach((card) => {
    const categoryMatches = activeCategory === 'all' || card.dataset.category === activeCategory;
    const searchText = `${card.dataset.search} ${card.textContent}`.toLowerCase();
    const searchMatches = query === '' || searchText.includes(query);
    const visible = categoryMatches && searchMatches;
    card.hidden = !visible;
    if (visible) visibleCount += 1;
  });

  emptyState.hidden = visibleCount !== 0;
}

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    activeCategory = button.dataset.category;
    filterButtons.forEach((item) => {
      const selected = item === button;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    applyCourseFilters();
  });
});

searchInput.addEventListener('input', applyCourseFilters);

function openCourseDialog(courseName) {
  dialogTitle.textContent = courseName;
  dialogDescription.textContent = `${courseName} is a sample learning path with short lessons, key concepts and practical activities. This demonstration shows the course discovery experience; it does not enrol users or store progress.`;
  courseDialog.showModal();
}

document.querySelectorAll('[data-course]').forEach((button) => {
  button.addEventListener('click', () => openCourseDialog(button.dataset.course));
});

function closeCourseDialog() {
  courseDialog.close();
}

dialogClose.addEventListener('click', closeCourseDialog);
dialogDone.addEventListener('click', closeCourseDialog);
courseDialog.addEventListener('click', (event) => {
  if (event.target === courseDialog) closeCourseDialog();
});

document.querySelectorAll('.nav-link, .header-cta, .hero-actions a').forEach((link) => {
  link.addEventListener('click', () => {
    const label = link.textContent.trim();
    if (label.toLowerCase().includes('course') || label.toLowerCase().includes('learning')) {
      toast.textContent = 'Explore the learning paths below.';
      toast.classList.add('show');
      window.clearTimeout(toastTimeout);
      toastTimeout = window.setTimeout(() => toast.classList.remove('show'), 1800);
    }
  });
});
