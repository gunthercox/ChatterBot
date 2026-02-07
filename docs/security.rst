========
Security
========

**Deploying chat bots to production environments requires due diligence,
especially in cases where LLMs are involved. At minimum, the following
precautions should be considered:**

* Comprehensive security review
* Additional rate limiting and abuse prevention
* Monitoring and alerting for security violations
* Regular security audits and penetration testing
* Understanding of the OWASP Top 10 for LLM Applications

Overview
========

When using ChatterBot, you may want to add security scanning to protect
against common vulnerabilities outlined in the `OWASP Top 10 for LLM Applications 
<https://owasp.org/www-project-top-10-for-large-language-model-applications/>`_.

ChatterBot does not include built-in security scanning. Instead, you can integrate
third-party security tools like `llm-guard <https://protectai.github.io/llm-guard/>`_,
`Prompt-Guard`_, or other scanning solution at the application level to scan inputs
before they reach the chatbot and outputs before they are shown to users.

**Depending on your use case, the following are examples of best practices you might consider:**

1. **Always scan user input** for prompt injection
2. **Always scan bot output** scan bot output to prevent PII leakage
3. **Start with strict thresholds** and relax if false positives occur
4. **Log security violations** for monitoring and analysis
5. **Test with adversarial inputs** before deployment
6. **Implement rate limiting** at application layer
7. **Never execute LLM outputs** as code without validation
8. **Review OWASP LLM Top 10** regularly

Additional Resources
====================

* `llm-guard Documentation <https://protectai.github.io/llm-guard/>`_
* `OWASP Top 10 for LLM Applications <https://owasp.org/www-project-top-10-for-large-language-model-applications/>`_
* `ProtectAI GitHub <https://github.com/protectai/llm-guard>`_
* `ChatterBot LLM Documentation <large-language-models.html>`_
* `Prompt-Guard <https://huggingface.co/meta-llama/Prompt-Guard-86M>`_
