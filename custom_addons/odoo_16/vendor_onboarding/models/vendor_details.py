from odoo import models, fields, api, _
from odoo.exceptions import UserError


class VendorDetails(models.TransientModel):
    _name = 'vendor.details'
    _description = 'Vendor details'
    _transient_max_hours = 720

    name = fields.Char(string='Name', required=True)
    contact_number = fields.Char(string='Contact number', required=True)
    address = fields.Text(string='Address', required=True)
    company_name = fields.Char(string='Company name', required=True)
    signup_id = fields.Many2many('signup', string='Signup record', required=True)
    state = fields.Selection([
        ('draft','Draft'),
        ('in_review','In Review'),
        ('1st_level_approved','1st level approved'),
        ('2nd_level_approved','2nd level approved'),
        ('rejected','Rejected'),
        ('approved','Approved'),
    ],string='Approval status', default='draft')


    @api.model
    def create(self, vals):
        record=super(VendorDetails, self).create(vals)
        record.submit_for_review()
        return record

    def submit_for_review(self):
        """Move to 'in_review' state and send email to Level 1 Approval group."""
        if self.state != 'draft':
            raise UserError(_("Only draft records can be submitted for review."))

        self.state = 'in_review'

        # Find users in Level 1 Approval group
        group = self.env.ref('vendor_onboarding.level1_approval_group', raise_if_not_found=False)
        if not group:
            raise UserError(_("The Level 1 Approval group is not configured."))

        # Get email addresses of the group's users
        emails = group.users.mapped('email')
        if not emails:
            raise UserError(_("No email addresses found for the Level 1 Approval group users."))


            # Fallback to manual email composition if no template is available
        for email in emails:
            body_html = f"""
                            <p>Dear Level 1 Approver,</p>
                           <p>A vendor profile is awaiting your review.</p>
                           <p><strong>Vendor Name:</strong> {self.name}</p>
                           <p><strong>Company:</strong> {self.company_name}</p>
                           <p><a href="/web#id={self.id}&model=vendor.details&view_type=form" target="_blank">
                               Click here to review the profile.
                           </a></p>
                           <p>Regards,<br/>Vendor Management System</p>
                            """

            mail_values = {
                'subject': _("Vendor Profile Review Required"),
                'body_html': body_html,
                'email_to': email,
                'email_from': 'neamul.bhuiyan@bjitgroup.com',  # Replace with your configured email
            }

            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.send()

        return True

    def approve_level_1(self):
        """Approve at Level 1."""
        if self.state != 'in_review':
            raise UserError(_("Only records in 'In Review' state can be approved at Level 1."))
        self.state = '1st_level_approved'

        # Find users in Level 2 Approval group
        group = self.env.ref('vendor_onboarding.level2_approval_group', raise_if_not_found=False)
        if not group:
            raise UserError(_("The Level 2 Approval group is not configured."))

        # Get email addresses of the group's users
        emails = group.users.mapped('email')
        if not emails:
            raise UserError(_("No email addresses found for the Level 2 Approval group users."))

            # Fallback to manual email composition if no template is available
        for email in emails:
            body_html = f"""
                                           <p>Dear Level 2 Approver,</p>
                                          <p>A vendor profile is awaiting your review.</p>
                                          <p><strong>Vendor Name:</strong> {self.name}</p>
                                          <p><strong>Company:</strong> {self.company_name}</p>
                                          <p><a href="/web#id={self.id}&model=vendor.details&view_type=form" target="_blank">
                                              Click here to review the profile.
                                          </a></p>
                                          <p>Regards,<br/>Vendor Management System</p>
                                           """

            mail_values = {
                'subject': _("Vendor Profile Review Required"),
                'body_html': body_html,
                'email_to': email,
                'email_from': 'neamul.bhuiyan@bjitgroup.com',  # Replace with your configured email
            }

            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.send()

    def reject_level_1(self):
        """Reject at Level 1."""
        if self.state != 'in_review':
            raise UserError(_("Only records in 'In Review' state can be rejected at Level 1."))
        self.state = 'rejected'

    def approve_level_2(self):
        """Approve at Level 2."""
        if self.state != '1st_level_approved':
            raise UserError(_("Only records in '1st Level Approved' state can be approved at Level 2."))
        self.state = '2nd_level_approved'


    def reject_level_2(self):
        """Reject at Level 2."""
        if self.state != '1st_level_approved':
            raise UserError(_("Only records in '1st Level Approved' state can be rejected at Level 2."))
        self.state = 'rejected'