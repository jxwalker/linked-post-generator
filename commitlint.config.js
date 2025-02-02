module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Enforce our custom commit message format if desired:
    'header-max-length': [2, 'always', 100],
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'refactor', 'test', 'chore']
    ]
  }
};