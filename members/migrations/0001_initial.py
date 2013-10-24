# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Member'
        db.create_table(u'members_member', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('is_superuser', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('username', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('is_staff', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('rin', self.gf('django.db.models.fields.IntegerField')(max_length=9, null=True, blank=True)),
        ))
        db.send_create_signal(u'members', ['Member'])

        # Adding M2M table for field groups on 'Member'
        m2m_table_name = db.shorten_name(u'members_member_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('member', models.ForeignKey(orm[u'members.member'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['member_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'Member'
        m2m_table_name = db.shorten_name(u'members_member_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('member', models.ForeignKey(orm[u'members.member'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['member_id', 'permission_id'])

        # Adding model 'MeetingAttendance'
        db.create_table(u'members_meetingattendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'members', ['MeetingAttendance'])

        # Adding model 'WorkHour'
        db.create_table(u'members_workhour', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('hours', self.gf('django.db.models.fields.DecimalField')(max_digits=3, decimal_places=2)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'members', ['WorkHour'])

        # Adding model 'ClassAttendance'
        db.create_table(u'members_classattendance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'members', ['ClassAttendance'])

        # Adding model 'Exam'
        db.create_table(u'members_exam', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('type', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('passed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'members', ['Exam'])

        # Adding model 'Show'
        db.create_table(u'members_show', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('host', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('genre', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('start_day', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('start_time', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('end_day', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('end_time', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('scheduled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shadowable', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'members', ['Show'])

        # Adding model 'Shadow'
        db.create_table(u'members_shadow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Member'])),
            ('show', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['members.Show'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'members', ['Shadow'])


    def backwards(self, orm):
        # Deleting model 'Member'
        db.delete_table(u'members_member')

        # Removing M2M table for field groups on 'Member'
        db.delete_table(db.shorten_name(u'members_member_groups'))

        # Removing M2M table for field user_permissions on 'Member'
        db.delete_table(db.shorten_name(u'members_member_user_permissions'))

        # Deleting model 'MeetingAttendance'
        db.delete_table(u'members_meetingattendance')

        # Deleting model 'WorkHour'
        db.delete_table(u'members_workhour')

        # Deleting model 'ClassAttendance'
        db.delete_table(u'members_classattendance')

        # Deleting model 'Exam'
        db.delete_table(u'members_exam')

        # Deleting model 'Show'
        db.delete_table(u'members_show')

        # Deleting model 'Shadow'
        db.delete_table(u'members_shadow')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'members.classattendance': {
            'Meta': {'object_name': 'ClassAttendance'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'members.exam': {
            'Meta': {'object_name': 'Exam'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'passed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'members.meetingattendance': {
            'Meta': {'object_name': 'MeetingAttendance'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'members.member': {
            'Meta': {'object_name': 'Member'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'rin': ('django.db.models.fields.IntegerField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'members.shadow': {
            'Meta': {'object_name': 'Shadow'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'show': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Show']"})
        },
        u'members.show': {
            'Meta': {'object_name': 'Show'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_day': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'end_time': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'genre': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'host': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scheduled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shadowable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'start_day': ('django.db.models.fields.IntegerField', [], {'max_length': '1'}),
            'start_time': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'members.workhour': {
            'Meta': {'object_name': 'WorkHour'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'hours': ('django.db.models.fields.DecimalField', [], {'max_digits': '3', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['members.Member']"})
        }
    }

    complete_apps = ['members']