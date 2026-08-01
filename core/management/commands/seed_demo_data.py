from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from services.models import Service
from core.models import Testimonial, FAQ, TeamMember
from blog.models import BlogPost

User = get_user_model()


class Command(BaseCommand):
    help = "Seeds the database with demo content for Munib and Co (services, FAQs, testimonials, team, a sample blog post)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        services = [
            ("Income Tax Filing", "bi-receipt",
             "Accurate, on-time filing of your annual income tax returns for individuals and businesses.",
             "Complete preparation and e-filing of income tax returns with the FBR, including salary, business and property income, deductions, and wealth statements. We review two years of prior filings to catch and correct errors before submission.",
             "Starting from PKR 5,000"),
            ("Sales Tax Filing", "bi-cash-coin",
             "Monthly sales tax return preparation and filing for registered businesses.",
             "We handle monthly and quarterly sales tax return filing, input/output tax reconciliation, and liaison with the FBR sales tax department so your business stays compliant without missed deadlines.",
             "Starting from PKR 6,000/month"),
            ("Company Incorporation (SECP)", "bi-building",
             "End-to-end company registration with the Securities and Exchange Commission of Pakistan.",
             "From name reservation to digital signature, memorandum and articles of association, and final incorporation certificate — we manage the full SECP registration process for private limited companies, SMCs and partnerships.",
             "Starting from PKR 15,000"),
            ("NTN & STRN Registration", "bi-card-checklist",
             "Get your National Tax Number and Sales Tax Registration Number issued quickly and correctly.",
             "We prepare and submit your NTN and STRN applications with all required supporting documents, and follow up with FBR until registration is confirmed.",
             "Starting from PKR 3,000"),
            ("Bookkeeping & Accounting", "bi-journal-text",
             "Monthly bookkeeping, ledger maintenance and financial statement preparation.",
             "Ongoing recording of transactions, bank reconciliations, ledger maintenance and preparation of monthly or quarterly financial statements, tailored to the size of your business.",
             "Starting from PKR 8,000/month"),
            ("Internal & External Audit", "bi-search",
             "Independent audit services that satisfy statutory, bank and stakeholder requirements.",
             "Our audit team conducts internal control reviews and statutory external audits in line with applicable financial reporting standards, with a clear management letter of findings.",
             "Quote on request"),
            ("FBR, SECP & PRA Compliance", "bi-shield-check",
             "Ongoing regulatory compliance management so you never miss a statutory deadline.",
             "We track and manage your recurring filing obligations across FBR, SECP and PRA — including annual returns, withholding statements and provincial sales tax on services — and alert you well before each deadline.",
             "Starting from PKR 10,000/month"),
            ("Tax Consultancy", "bi-people",
             "Strategic tax planning and advisory for individuals, startups and growing businesses.",
             "One-on-one consultancy covering tax planning, structuring, exemptions and notices/appeals handling, so you make informed decisions before, not after, a filing.",
             "PKR 3,000/session"),
        ]
        for i, (title, icon, short_desc, desc, fee) in enumerate(services):
            Service.objects.update_or_create(
                title=title,
                defaults=dict(icon=icon, short_description=short_desc, description=desc, fee_note=fee, order=i, is_active=True),
            )
        self.stdout.write(self.style.SUCCESS(f"  {len(services)} services created/updated"))

        faqs = [
            ("Do I need to file a tax return if my income is below the taxable limit?",
             "Filing is still required to become an Active Taxpayer, which gives you lower withholding tax rates on banking, property and vehicle transactions, even if no tax is payable."),
            ("How long does SECP company incorporation take?",
             "Typically 5-10 working days once all required documents (CNICs, digital signatures, proposed name, MOA/AOA) are submitted, subject to SECP processing times."),
            ("What documents do I need for income tax filing?",
             "CNIC, salary certificate or business income details, bank statements, property documents (if any), and last year's tax return if available. We'll send you a checklist after booking."),
            ("Can you handle FBR notices and audits on my behalf?",
             "Yes. We represent clients in FBR notices, audits and appeals, preparing all required responses and supporting documentation."),
            ("Do you work with businesses outside Swat?",
             "Yes, we serve clients across Pakistan remotely, with document exchange handled securely online, plus in-person meetings for local clients."),
        ]
        for i, (q, a) in enumerate(faqs):
            FAQ.objects.update_or_create(question=q, defaults=dict(answer=a, order=i, is_active=True))
        self.stdout.write(self.style.SUCCESS(f"  {len(faqs)} FAQs created/updated"))

        testimonials = [
            ("Asfand Yar Khan", "Owner, Swat Textiles", "Munib and Co filed three years of overdue returns for us without a single error flagged by FBR. Genuinely careful people.", 5),
            ("Sana Gul", "Freelance Consultant", "Registration for my NTN and first tax return was handled start to finish. I never had to chase them for updates.", 5),
            ("Imran Bacha", "Director, Bacha Traders (Pvt) Ltd", "Our SECP incorporation was done faster than we expected, and the fee structure was clear from day one.", 4),
        ]
        for name, designation, content, rating in testimonials:
            Testimonial.objects.update_or_create(client_name=name, defaults=dict(designation=designation, content=content, rating=rating, is_active=True))
        self.stdout.write(self.style.SUCCESS(f"  {len(testimonials)} testimonials created/updated"))

        team = [
            ("Munib Ur Rahman", "Founder & Chartered Accountant", "Leads the firm's tax and audit practice with over 15 years of experience serving SMEs across Khyber Pakhtunkhwa.", 0),
            ("Zahid Haroon", "Senior Tax Consultant", "Specialises in FBR compliance, tax planning and appeals for individual and corporate clients.", 1),
            ("Ayesha Noor", "Bookkeeping & Accounts Lead", "Manages monthly bookkeeping and financial statement preparation for retainer clients.", 2),
        ]
        for name, designation, bio, order in team:
            TeamMember.objects.update_or_create(name=name, defaults=dict(designation=designation, bio=bio, order=order, is_active=True))
        self.stdout.write(self.style.SUCCESS(f"  {len(team)} team members created/updated"))

        admin_user = User.objects.filter(is_superuser=True).first()
        if not BlogPost.objects.exists():
            BlogPost.objects.create(
                title="FBR Tax Filing Deadline: What You Need to Know This Year",
                category="tax",
                excerpt="A quick guide to the annual income tax filing deadline, extensions, and penalties for late filing.",
                content=(
                    "Every year, individuals and businesses across Pakistan are required to file their income tax "
                    "returns by the FBR deadline. Missing this deadline can result in penalties and being removed "
                    "from the Active Taxpayers List, which increases withholding tax rates on everyday transactions.\n\n"
                    "Our advice is simple: start gathering your documents early, keep bank statements and salary "
                    "certificates on hand, and book a consultation well before the deadline so there's time to "
                    "resolve any discrepancies.\n\n"
                    "If you've missed a previous year's filing, it's not too late to catch up. We regularly help "
                    "clients file backlogged returns and get back on the Active Taxpayers List."
                ),
                author=admin_user,
                is_published=True,
                published_at=timezone.now(),
            )
            self.stdout.write(self.style.SUCCESS("  1 sample blog post created"))

        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))
