#
# Copyright 2010 BengDict Project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.views.generic.list_detail import object_list, object_detail
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Contributor
from .forms import ProfileForm

def contributor_list(request):
    return object_list(request, Contributor.objects.order_by('number_words'),
                       template_object_name='contributor', paginate_by=50)

@login_required
def contributor_edit(request):
    profile = request.user.get_or_create_profile()
    if request.method == 'POST':
        form = ProfileForm(data=request.POST)
        if form.is_valid():
            profile.user.first_name = form.cleaned_data['fullname']
            profile.user.save()
            profile.website = form.cleaned_data['website']
            profile.ims = form.cleaned_data['ims']
            profile.save()
    else:
        form = ProfileForm(initial={'fullname': request.user.first_name,
                                    'website': profile.website, 'ims':
                                    profile.ims})

    context = {'form': form, 'profile': profile}
    return render_to_response('contributor/edit.html', context,
                              RequestContext(request))


def contributor_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user == request.user:
        return HttpResponseRedirect(reverse('contributor_edit'))

    profile = user.get_or_create_profile()
    return render_to_response('contributor/profile.html', {'profile': profile},
                              RequestContext(request))