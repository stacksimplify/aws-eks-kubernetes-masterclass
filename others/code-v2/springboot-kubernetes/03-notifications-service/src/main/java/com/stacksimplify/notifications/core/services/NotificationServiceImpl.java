package com.stacksimplify.notifications.core.services;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;

import javax.mail.MessagingException;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.env.Environment;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.MimeMessageHelper;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import com.stacksimplify.notifications.core.dtos.EmailMessage;

@Service
public class NotificationServiceImpl implements NotificationService {

	private static final Logger logger = LoggerFactory.getLogger(NotificationServiceImpl.class);

	@Autowired
	JavaMailSender mailSender;
	
	@Autowired
	private Environment env;


	@Override
	@Async("threadPoolExecutor")
	public void sendEmail(EmailMessage emailMessage) {
		logger.info("Preparing to send email.");
		ArrayList<InternetAddress> toEmails = prepareUniqueEmailList(emailMessage.getToEmails());
		ArrayList<InternetAddress> ccEmails = prepareUniqueEmailList(emailMessage.getCcEmails());
		ArrayList<InternetAddress> bccEmails = prepareUniqueEmailList(emailMessage.getBccEmails());
		logger.info("Unique emails list for to, cc, bcc created.");

		MimeMessage message = mailSender.createMimeMessage();
		MimeMessageHelper messageHelper = null;
		
		String fromAddress = env.getProperty("mail.server.from.address");
		try {
			messageHelper = new MimeMessageHelper(message, true);
			messageHelper.setTo(toEmails.toArray(new InternetAddress[toEmails.size()]));
			messageHelper.setCc(ccEmails.toArray(new InternetAddress[ccEmails.size()]));
			messageHelper.setBcc(bccEmails.toArray(new InternetAddress[bccEmails.size()]));
			messageHelper.setSubject(emailMessage.getSubject());
			messageHelper.setText(emailMessage.getContent());
			messageHelper.setFrom(fromAddress);
			logger.info("Email prepared.");

			mailSender.send(message);
			logger.info("Email sent successfully.");
		} catch (MessagingException e) {
			logger.error("Error encountered in sending email, ", e);
		}

	}

	public ArrayList<InternetAddress> prepareUniqueEmailList(List<String> emails) {
		Set<String> uniqueEmails = new TreeSet<String>(String.CASE_INSENSITIVE_ORDER);
		if (emails != null) {
			uniqueEmails.addAll(emails);
		}

		ArrayList<InternetAddress> uniqueEmailList = new ArrayList<>();
		for (String email : uniqueEmails) {
			logger.info(email);
			InternetAddress i = new InternetAddress();
			i.setAddress(email);
			uniqueEmailList.add(i);
		}
		logger.info("Unique email list prepared successfully.");
		return uniqueEmailList;
	}

}
